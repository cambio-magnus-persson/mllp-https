### Added feature: MLLP to HTTPS
### By Tiago Rodrigues
### Sectra Iberia, Aug 2022
### Addapted from https://github.com/rivethealth/mllp-http
import base64
import datetime
import functools
import logging
import os
from datetime import datetime, timezone

import requests
import socket
import socketserver
import urllib

from requests.auth import HTTPBasicAuth

from .mllp import read_mllp, write_mllp
from .net import read_socket_bytes
from .version import __version__

logger = logging.getLogger(__name__)


def display_address(address):
    return f"{address[0]}:{address[1]}"


class MllpServerOptions:
    def __init__(self, timeout):
        self.timeout = timeout


class MllpHandler(socketserver.StreamRequestHandler):
    # Class for parsing HL7 data as MLLP Server and send it to a host as a HTTPS Client

    def __init__(self, request, address, server, timeout, https_url, https_options):
        self.https_url = https_url
        self.https_options = https_options
        self.timeout = timeout

        # If username and password are provided as arguments, use authentication
        self.username = https_options.username
        self.password = https_options.password
        self.certfile = https_options.certfile
        self.keyfile = https_options.keyfile
        self.auth = None
        if self.username and self.password:
            self.auth = ''
            self.auth = 'Basic ' + base64.b64encode(
                bytes('%s:%s' % (self.username, self.password), 'utf-8')).decode('ascii')
        super().__init__(request, address, server)

    def handle(self):
        if self.timeout:
            self.request.settimeout(self.timeout)
        self.request.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 10)

        # Session for HTTPS persistent connection
        session = requests.Session()

        # >> Notes on dealing with SSL:
        # Requests verifies SSL certificates for HTTPS requests.
        # By default, SSL verification is enabled, and Requests will
        # throw a SSLError if it’s unable to verify the certificate
        #
        # The private key to the local certificate must be unencrypted.
        # Currently, Requests does not support using encrypted keys.
        #
        # https://requests.readthedocs.io/en/latest/user/advanced/

        local_address = self.request.getsockname()
        remote_address = self.request.getpeername()

        stream = read_socket_bytes(self.rfile)

        try:
            for message in read_mllp(stream):
                try:
                    logger.info("Message: %s bytes", len(message))
                    logger.info("Received Data:\n{}\n\n".format(message))
                    headers = {
                        "Forwarded": f"by={display_address(local_address)};for={display_address(remote_address)};proto=mllp",
                        "User-Agent": f"mllp2http/{__version__}",
                        "X-Forwarded-For": display_address(remote_address),
                        "X-Forwarded-Proto": "mllp",
                    }

                    if self.auth:
                        headers["Authorization"] = self.auth
                        #print("Authorization: {}".format(self.auth))
                    elif os.environ.get("HTTP_AUTHORIZATION"):
                        headers["Authorization"] = os.environ["HTTP_AUTHORIZATION"]
                        #print("Authorization: {}".format(os.environ["HTTP_AUTHORIZATION"]))
                    if os.environ.get("API_KEY"):
                        headers["X-API-KEY"] = os.environ["API_KEY"]
                        # print(os.environ["API_KEY"])

                    if self.https_options.content_type is not None:
                        headers["Content-Type"] = self.https_options.content_type

                    now = datetime.now(timezone.utc)
                    date = now.strftime("%a, %d %b %y %H:%M:%S %Z")
                    headers["Date"] = date

                    # Disabled the warning because it was causing the program to freeze
                    if not self.https_options.verify:
                        logger.warning("Verify SSL: " + str(self.https_options.verify))
                        requests.packages.urllib3.disable_warnings()

                    # Sending the HL7 data by HTTPS by POST Method
                    response = session.post(
                        urllib.parse.urlunparse(self.https_url),
                        data=message,
                        headers=headers,
                        timeout=self.https_options.timeout,
                        verify=self.https_options.verify,  # To verify server SSL/TLS certificate. Keep as False only
                        # when using a self-sign certificate since the library does not allow self-signed certificates
                        cert=(self.certfile, self.keyfile)
                    )
                    response.raise_for_status()  # Get ACK response
                except requests.exceptions.HTTPError as e:
                    logger.error("HTTPS response error: %s", e.response.status_code)
                    break
                except Exception as e:
                    logger.error("HTTPS connection error: %s", e)
                    break
                else:
                    content = response.content
                    # print(content.decode())
                    logger.info("Response: %s bytes", len(content))
                    logger.info("Response Data:\n{}\n\n".format(content.decode()))
                    write_mllp(self.wfile, content)
                    self.wfile.flush()
        except ConnectionResetError as e:
            # An enception was raised when the MLLP client closed the connection on their side
            logger.info("MLLP Server Disconnected")
        except Exception as e:
            logger.error("Failed read MLLP message: %s", e)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


class HttpsClientOptions:
    def __init__(self, content_type, timeout, verify, username, password, certfile, keyfile):
        self.content_type = content_type
        self.timeout = timeout
        self.verify = True
        if verify == "False":
            self.verify = False
        elif verify == "True":
            self.verify = True
        else:
            self.verify = verify
        self.username = username
        self.password = password
        self.certfile = certfile
        self.keyfile = keyfile


def serve(address, options, https_url, https_options):
    logger = logging.getLogger(__name__)

    # Handler for parsing the data from the MLLP socket
    handler = functools.partial(
        MllpHandler,
        https_url=https_url,
        https_options=https_options,
        timeout=options.timeout or None,
    )

    try:
        # MLLP Server/Listener
        server = ThreadedTCPServer(address, handler)

        logger.info("Listening on %s:%s", address[0], address[1])
        logger.info("Sending to %s", https_url[1])
        print("\nListening on {}:{}".format(address[0], address[1]))
        print("Sending to {}".format(https_url[1]))
        server.serve_forever()

    except Exception as e:
        logger.error("MLLP connection error: %s", e)
