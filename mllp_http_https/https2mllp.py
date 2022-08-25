### Added feature: HTTPS to MLLP
### By Tiago Rodrigues
### Sectra Iberia, Aug 2022
### Addapted from https://github.com/rivethealth/mllp-http

import functools
import http.server
import logging
import socket
import ssl
import threading
import time
from .mllp import send_mllp

logger = logging.getLogger(__name__)


class MllpClientOptions:
    def __init__(self, keep_alive, max_messages, timeout):
        #self.address = address
        self.keep_alive = keep_alive
        self.max_messages = max_messages
        self.timeout = timeout


class MllpClient:
    def __init__(self, address, options):
        self.address = address
        self.options = options
        self.connections = []
        self.lock = threading.Lock()

    def _check_connection(self, connection):
        while not connection.closed:
            elasped = (
                connection.last_update - time.monotonic()
                if connection.last_update is not None
                else 0
            )
            remaining = self.options.keep_alive + elasped
            if 0 < remaining:
                time.sleep(remaining)
            else:
                try:
                    with self.lock:
                        self.connections.remove(connection)
                except ValueError:
                    pass
                else:
                    if self.options.keep_alive > 0:
                        # To keep the connection alive in case keep_alive is -1
                        connection.close()

    def _connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.options.timeout:
            s.settimeout(self.options.timeout)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 10)
        print(self.address)
        s.connect(self.address)
        connection = MllpConnection(s)
        if self.options.keep_alive is not None:
            thread = threading.Thread(
                daemon=False,
                target=self._check_connection,
                args=(connection, )
            )
            thread.start()
        return connection

    def send(self, data):
        with self.lock:
            try:
                connection = self.connections.pop()
            except IndexError:
                connection = None
            else:
                connection.last_update = None
        if connection is None:
            connection = self._connect()
        response = connection.send(data)
        if self.options.max_messages <= connection.message_count and self.options.max_messages >= 0:
            connection.close()
        else:
            connection.last_update = time.monotonic()
            with self.lock:
                self.connections.append(connection)
        return response


class MllpConnection:
    def __init__(self, socket):
        self.closed = False
        self.last_update = None
        self.message_count = 0
        self.socket = socket

    def close(self):
        self.close = True
        self.socket.shutdown(2)
        self.socket.close()
        print("Disconnected from MLLP Server")

    def send(self, data):
        self.message_count += 1

        # To send the HL7 messages, it will make use of an MLLP parser to format the data
        # The parser will return the ACK/NACK response
        return send_mllp(self.socket, data)


class HttpsServerOptions:
    def __init__(self, timeout, content_type, certfile, keyfile, keep_alive):
        self.timeout = timeout
        self.content_type = content_type
        self.certfile = certfile
        self.keyfile = keyfile
        self.keep_alive = keep_alive


class HttpsHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, request, address, server, mllp_client, content_type, timeout, keep_alive):
        self.content_type = content_type
        self.mllp_client = mllp_client
        self.timeout = timeout
        self.keep_alive = keep_alive
        super().__init__(request, address, server)


    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        logger.info("Message: %s bytes", len(data))
        print("Received Data:\n{}".format(data))
        response = self.mllp_client.send(data)
        logger.info("Response: %s bytes", len(response))
        self.send_response(201)
        self.send_header("Content-Length", len(response))
        if self.content_type:
            self.send_header("Content-Type", self.content_type)
        if self.keep_alive is not None:
            self.send_header("Keep-Alive", f"timeout={self.keep_alive}")
        self.end_headers()
        self.wfile.write(response)


def serve(address, options, mllp_address, mllp_options):
    # MLLP Client for dealing with the MLLP TCP connection
    client = MllpClient(mllp_address, mllp_options)

    # HTTP server handler
    handler = functools.partial(
        HttpsHandler,
        content_type=options.content_type,
        keep_alive=options.keep_alive,
        timeout=options.timeout or None,
        mllp_client=client,
    )

    server = http.server.ThreadingHTTPServer(address, handler)

    # >> Dealing with SSL/TLS on the HTTP server side
    # For Python > 3.7
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain(
        certfile=options.certfile,
        keyfile=options.keyfile,
    )
    server.socket = context.wrap_socket(
        server.socket,
        server_side=True,
    )
    # For Python < 3.2
    # server.socket = ssl.wrap_socket(
    #     server.socket,
    #     server_side=True,
    #     certfile="C:/ssl/certfile.crt",
    #     keyfile="C:/ssl/keyfile.key",
    # )

    logger.info("\nListening on %s:%s", address[0], address[1])
    server.protocol_version = "HTTP/1.1"
    server.serve_forever()
