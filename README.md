# MLLP/HTTP(S)

[![PyPI](https://img.shields.io/pypi/v/mllp-https)](https://pypi.org/project/mllp-https/)


[Project](https://github.com/tiagoepr/mllp-https/) addapted by: Tiago Rodrigues, 2022 <br>

This project results of an enhanced package supporting HTTPS of the [original project](https://pypi.org/project/mllp-http/), whose original credits are given to [Rivet Health](https://pypi.org/user/rivet/)



<p align="center">
  <img src="https://github.com/tiagoepr/mllp-https/raw/master/doc/logo.png">
</p>

## Overview

Convert MLLP to HTTP(S) and vice versa.

`http2mllp` is a HTTP server that translates to MLLP.

`mllp2http` is a MLLP server that translates to HTTP.

`https2mllp` is a HTTPS server that translates to MLLP.

`mllp2https` is a MLLP server that translates to HTTPS.

Keywords: MLLP, HTTP, HTTPS, SSL/TLS, HL7

## Description

MLLP (Minimum Lower Layer Protocol) is the traditional session protocol for HL7
messages.

Many modern tools (load balancers, application frameworks, API monitoring) are
designed around HTTP(S). This observation is the foundation for the
[HL7 over HTTP](https://hapifhir.github.io/hapi-hl7v2/hapi-hl7overhttp/specification.html)
specification.

This project, MLLP/HTTP(S), bridges these two protocols, allowing network engineers
and application developers to work with familiar HTTP(S) technology while
interfacing with MLLP-based programs.

Implements
[MLLP release 1](https://www.hl7.org/documentcenter/public/wg/inm/mllp_transport_specification.PDF), [HTTP/1.1](https://tools.ietf.org/html/rfc2616), and SSL/TLS (optional). Each MLLP message is
assumed to have a corresponding response message (e.g. HL7 acknoledgment).

Note that this project deals only with the MLLP layer; it does not process HL7
messages themselves. Notably, the HTTP participant must be able to intepret HL7
messages and generate acknowledgements. This separation imposes no requirements
for HL7 usage and leaves application developers with full access to the features
of the HL7 protocol.

## Install


### By [Pip](https://pypi.org/project/awscli-saml/)
```sh
pip install mllp-https
```

### By Command Line
On the project folder, run the command:
```sh
python setup.py install
```



## Run as
### Command Line
```sh
http2mllp localhost

mllp2http http://localhost:8000

https2mllp localhost

mllp2https https://localhost:8000
```

#### Notes on SSL/TLS:
To use https2mllp as a https server/listener, it is required to provide a valid path for SSL certificate file and private key file. In order to do that, both certificate and key files should be placed on a folder "C:/ssl/", such that the files' paths are "C:/ssl/certfile.crt" and "C:/ssl/keyfile.key". Otherwise, both paths should be passed as argument:
```sh
https2mllp localhost --mllp_port 2575 --certfile /PATH/TO/certfile.crt --keyfile /PATH/TO/keyfile.key
```

### [Docker](https://hub.docker.com/r/tiagoepr/mllp-https)
Pull from Docker Hub:
```sh
docker pull tiagoepr/mllp-https
```
or build from dockerfile:
```sh
docker build -t tiagoepr/mllp-https .
```


Run as:

```sh
docker run -it -p 8000:8000 --rm tiagoepr/mllp-https http2mllp host.docker.internal

docker run -it -p 2575:2575 --rm tiagoepr/mllp-https mllp2http http://host.docker.internal:8000

docker run -it -p 8000:8000 --rm tiagoepr/mllp-https https2mllp host.docker.internal (See note below about SSL certificate)

docker run -it -p 2575:2575 --rm tiagoepr/mllp-https mllp2https https://host.docker.internal:8000
```
#### Notes on SSL/TLS:
To use https2mllp as a https server/listener, it is required to provide a valid path for SSL certificate file and private key file. In order to do that, both certificate and key files should be firstly copied onto the Docker container and then the respective paths given as argument.
<br>To do that, with the container running, run the command on the host:

```sh
docker cp [LOCAL/PATH/TO/ssl] [container_id]:/usr/local/lib/python3.10/site-packages/mllp_http_https/ssl
```
where [LOCAL/PATH/TO/ssh] is the path for the folder containing the certfile.crt and keyfile.key and [container_id] should be replaced by the container ID which is running.
<br>Now, on the container bash, run the command:
```sh
docker run -it -p 8000:8000 --rm tiagoepr/mllp-https https2mllp host.docker.internal --certfile /usr/local/lib/python3.7/site-packages/mllp_http_https/ssl/certfile.crt --keyfile /usr/local/lib/python3.7/site-packages/mllp_http_https/ssl/keyfile.key
```
## Usage

### http2mllp

```
usage: http2mllp [-h] [-H HOST] [-p PORT] [--keep-alive KEEP_ALIVE] [--log-level {error,warn,info}]
                 [--mllp-keep-alive MLLP_KEEP_ALIVE] [--mllp-max-messages MLLP_MAX_MESSAGES] [--mllp-release {1}]
                 [--timeout TIMEOUT] [--content-type CONTENT_TYPE] [-v] [--mllp_port MLLP_PORT]
                 mllp_url

            HTTP server that proxies an MLLP client.
            Expects an MLLP response message and uses it as the HTTP response.


positional arguments:
  mllp_url              MLLP URL, Defaulf: hostname

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  HTTP host (default: 0.0.0.0)
  -p PORT, --port PORT  HTTP port (default: 8000)
  --keep-alive KEEP_ALIVE
                        keep-alive in milliseconds, or unlimited if -1. (default: -1)
  --log-level {error,warn,info}
  --mllp-keep-alive MLLP_KEEP_ALIVE
                        keep-alive in milliseconds, or unlimited if -1. (default: -1)
  --mllp-max-messages MLLP_MAX_MESSAGES
                        maximum number of messages per connection, or unlimited if -1. (default: -1)
  --mllp-release {1}    MLLP release version (default: 1)
  --timeout TIMEOUT     socket timeout, in milliseconds, or unlimited if 0. (default: 0)
  --content-type CONTENT_TYPE
                        HTTP Content-Type header (default: x-application/hl7-v2+er7)
  -v, --version         show program's version number and exit
  --mllp_port MLLP_PORT
                        MLLP PORT (default: 2575)
```

### mllp2http

```
usage: mllp2https [-h] [-H HOST] [-p PORT] [--username USERNAME] [--password PASSWORD] [--content-type CONTENT_TYPE] [--log-level {error,warn,info}] [--log-file LOG_FILE] [--mllp-release {1}] [--timeout TIMEOUT] [--verify {False,True}]
                  [-v]
                  https_url

MLLP server that proxies an HTTPS client. Sends back the HTTPS response.

positional arguments:
  https_url             HTTPS URL

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  MLLP host (default: 0.0.0.0)
  -p PORT, --port PORT  MLLP port (default: 2575)
  --username USERNAME   Username for HTTPS server authentication (Optional). If not provided, authentication will be skipped. (default: None)
  --password PASSWORD   User password for HTTPS server authentication (Optional). If not provided, authentication will be skipped. (default: None)
  --content-type CONTENT_TYPE
                        HTTPS Content-Type header (default: application/hl7-v2; charset=utf-8)
  --log-level {error,warn,info}
  --log-file LOG_FILE   Path to file where the logs will be placed. If not provided logging will be done on command window. (default: None)
  --mllp-release {1}    MLLP release version (default: 1)
  --timeout TIMEOUT     timeout in milliseconds (default: 0)
  --verify {False,True}
                        Verify SSL certificate on server side. True as default (default: True)
  -v, --version         show program's version number and exit

environment variables:
    HTTP_AUTHORIZATION - HTTP Authorization header
    X-API-KEY - HTTP X-API-KEY header
```


### https2mllp
```
usage: https2mllp [-h] [-H HOST] [-p PORT] [--username USERNAME] [--password PASSWORD] [--keep-alive KEEP_ALIVE] [--log-level {error,warn,info}] [--log-folder LOG_FOLDER] [--mllp-keep-alive MLLP_KEEP_ALIVE]
                  [--mllp-max-messages MLLP_MAX_MESSAGES] [--mllp-release {1}] [--timeout TIMEOUT] [--content-type CONTENT_TYPE] [--mllp_port MLLP_PORT] [--certfile CERTFILE] [--keyfile KEYFILE] [--mllp_parser {True,False}] [-v]
                  mllp_url

            HTTPS server that proxies an MLLP client.
            Expects an MLLP response message and uses it as the HTTPS response.


positional arguments:
  mllp_url              MLLP URL, Defaulf: hostname

optional arguments:
  -h, --help            show this help message and exit
  --mllp_port MLLP_PORT
                        MLLP PORT (default: 2575)
  -H HOST, --host HOST  HTTPS host (default: 0.0.0.0)
  -p PORT, --port PORT  HTTPS port (default: 8000)
  --username USERNAME   Username for HTTPS server authentication (Optional). If not provided, authentication will be skipped unless the environment vartiable exists. (default: None)
  --password PASSWORD   User password for HTTPS server authentication (Optional). If not provided, authentication will be skipped  unless the environment vartiable exists. (default: None)
  --keep-alive KEEP_ALIVE
                        keep-alive in milliseconds, or unlimited if -1. (default: 0)
  --log-level {error,warn,info}
  --log-folder LOG_FOLDER   Path to folder where the logs will be placed. If not provided logging will be done on command window. (default: None)
  --mllp-keep-alive MLLP_KEEP_ALIVE
                        keep-alive in milliseconds, or unlimited if -1. (default: 10000)
  --mllp-max-messages MLLP_MAX_MESSAGES
                        maximum number of messages per connection, or unlimited if -1. (default: -1)
  --mllp-release {1}    MLLP release version (default: 1)
  --timeout TIMEOUT     socket timeout, in milliseconds, or unlimited if 0. (default: 0)
  --content-type CONTENT_TYPE
                        HTTPS Content-Type header (default: application/hl7-v2; charset=utf-8)
  --certfile CERTFILE   Path for HTTPS Server's SSL/TLS Certificate. (default: C:/ssl/certfile.crt)
  --keyfile KEYFILE     Path for HTTPS Server's SSL/TLS Private Key. (default: C:/ssl/keyfile.key)
  --mllp_parser {True,False}
                        If False, the package will not parse the MLLP and will send an HTTPS POST with the MLLP encapsulating the HL7 message. If True, the HTTPS POST will only present the HL7 on the Body without MLLP characters
                        (default: True)
  -v, --version         Show program's version number and exit
```


### mllp2https

```
usage: mllp2https [-h] [-H HOST] [-p PORT] [--username USERNAME] [--password PASSWORD] [--content-type CONTENT_TYPE] [--log-level {error,warn,info}] [--log-folder LOG_FOLDER] [--mllp-release {1}] [--timeout TIMEOUT] [--verify {False,True}]
                  [-v]
                  https_url

MLLP server that proxies an HTTPS client. Sends back the HTTPS response.

positional arguments:
  https_url             HTTPS URL

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  MLLP host (default: 0.0.0.0)
  -p PORT, --port PORT  MLLP port (default: 2575)
  --username USERNAME   Username for HTTPS server authentication (Optional). If not provided, authentication will be skipped. (default: None)
  --password PASSWORD   User password for HTTPS server authentication (Optional). If not provided, authentication will be skipped. (default: None)
  --content-type CONTENT_TYPE
                        HTTPS Content-Type header (default: application/hl7-v2; charset=utf-8)
  --certfile CERTFILE   Path for HTTPS Server's SSL/TLS Certificate.
  --keyfile KEYFILE     Path for HTTPS Server's SSL/TLS Private Key.
  --log-level {error,warn,info}
  --log-folder LOG_FOLDER   Path to folder where the logs will be placed. If not provided logging will be done on command window. (default: None)
  --mllp-release {1}    MLLP release version (default: 1)
  --timeout TIMEOUT     Timeout in milliseconds (default: 0)
  --verify {False,True}
                        Verify SSL certificate on server side. Should be set to 'True', 'False' or to a path to a CA_BUNDLE file or directory with certificates of trusted Cas.
  -v, --version         show program's version number and exit

environment variables:
    HTTPS_AUTHORIZATION - HTTPS Authorization header
    X-API-KEY - HTTPS X-API-KEY header

```



## Examples

### mllp2http

Run an HTTP debugging server:

```sh
docker run -p 8000:80 --rm kennethreitz/httpbin
```

Run the MLLP connector:

```sh
mllp2http http://localhost:8000
```

Send an MLLP message:

```sh
printf '\x0bMESSAGE\x1c\x0d' | socat - TCP:localhost:2575
```

and see the HTTP server's response (which describes the HTTP request that the
connector made):

```json
{
  "args": {},
  "data": "MESSAGE",
  "files": {},
  "form": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Content-Length": "7",
    "Content-Type": "x-application/hl7-v2+er7",
    "Forwarded": "by=127.0.0.1:2575;for=127.0.0.1:54572;proto=mllp",
    "Host": "localhost:8000",
    "User-Agent": "mllp2http/1.0.2"
  },
  "json": null,
  "origin": "127.0.0.1:54572",
  "url": "mllp://localhost:8000/post"
}
```

## Developing

To install:

```sh
make install
```

Before committing, format:

```sh
make format
```
