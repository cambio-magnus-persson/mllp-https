# MLLP/HTTP(S)

[![PyPI](https://img.shields.io/pypi/v/mllp-https)](https://pypi.org/project/mllp-https/)


[Project](https://github.com/tiagoepr/mllp-https/) addapted by: Tiago Rodrigues, SECTRA Iberia, 2022 <br>

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
```sh
http2mllp localhost --mllp_port 2575

mllp2http http://localhost:8000

https2mllp localhost --mllp_port 2575

mllp2https https://localhost:8000
```

### [Docker](https://hub.docker.com/r/tiagoepr/mllp-https)
```sh
docker pull tiagoepr/mllp-https
```

Run as

```sh
docker run -it -p 2575:2575 --rm tiagoepr/mllp-https http2mllp localhost --mllp_port 2575

docker run -it -p 2575:2575 --rm tiagoepr/mllp-https mllp2http http://localhost:8000

docker run -it -p 2575:2575 --rm tiagoepr/mllp-https https2mllp localhost --mllp_port 2575 

docker run -it -p 2575:2575 --rm tiagoepr/mllp-https mllp2http http://localhost:8000
```

## Usage

### http2mllp

```
usage: http2mllp [-h] [-H HOST] [-p PORT] [--keep-alive KEEP_ALIVE] [--log-level {error,warn,info}]
                 [--mllp-keep-alive MLLP_KEEP_ALIVE] [--mllp-max-messages MLLP_MAX_MESSAGES] [--mllp-release {1}]
                 [--timeout TIMEOUT] [--content-type CONTENT_TYPE] [-v] [--mllp_port MLLP_PORT]
                 mllp_url

            HTTP server that proxies an MLLP server.
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
usage: mllp2http [-h] [-H HOST] [-p PORT] [--content-type CONTENT_TYPE] [--log-level {error,warn,info}] [--mllp-release {1}]
                 [--timeout TIMEOUT] [-v]
                 http_url

MLLP server that proxies an HTTP server. Sends back the HTTP response.

positional arguments:
  http_url              HTTP URL

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  MLLP host (default: 0.0.0.0)
  -p PORT, --port PORT  MLLP port (default: 2575)
  --content-type CONTENT_TYPE
                        HTTP Content-Type header (default: x-application/hl7-v2+er7)
  --log-level {error,warn,info}
  --mllp-release {1}    MLLP release version (default: 1)
  --timeout TIMEOUT     timeout in milliseconds (default: 0)
  -v, --version         show program's version number and exit

environment variables:
    HTTP_AUTHORIZATION - HTTP Authorization header
    API_KEY - HTTP X-API-KEY header
```


### https2mllp
```
usage: https2mllp [-h] [-H HOST] [-p PORT] [--keep-alive KEEP_ALIVE] [--log-level {error,warn,info}]
                  [--mllp-keep-alive MLLP_KEEP_ALIVE] [--mllp-max-messages MLLP_MAX_MESSAGES] [--mllp-release {1}]
                  [--timeout TIMEOUT] [--content-type CONTENT_TYPE] [--mllp_port MLLP_PORT] [--certfile CERTFILE]
                  [--keyfile KEYFILE] [-v]
                  mllp_url

            HTTPS server that proxies an MLLP server.
            Expects an MLLP response message and uses it as the HTTPS response.


positional arguments:
  mllp_url              MLLP URL, Defaulf: hostname

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  HTTPS host (default: 0.0.0.0)
  -p PORT, --port PORT  HTTPS port (default: 8000)
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
                        HTTPS Content-Type header (default: x-application/hl7-v2+er7)
  --mllp_port MLLP_PORT
                        MLLP PORT (default: 2575)
  --certfile CERTFILE   Path for HTTPS Server's SSL/TLS Certificate. Default: C:/ssl/certfile.crt (default:
                        C:/ssl/certfile.crt)
  --keyfile KEYFILE     Path for HTTPS Server's SSL/TLS Private Key. Default: C:/ssl/keyfile.key (default:
                        C:/ssl/keyfile.key)
  -v, --version         show program's version number and exit
```


### mllp2https

```
usage: mllp2https [-h] [-H HOST] [-p PORT] [--content-type CONTENT_TYPE] [--log-level {error,warn,info}]
                  [--mllp-release {1}] [--timeout TIMEOUT] [--verify {False,True}] [-v]
                  https_url

MLLP server that proxies an HTTPS server. Sends back the HTTPS response.

positional arguments:
  https_url             HTTPS URL

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  MLLP host (default: 0.0.0.0)
  -p PORT, --port PORT  MLLP port (default: 2575)
  --content-type CONTENT_TYPE
                        HTTPS Content-Type header (default: x-application/hl7-v2+er7)
  --log-level {error,warn,info}
  --mllp-release {1}    MLLP release version (default: 1)
  --timeout TIMEOUT     timeout in milliseconds (default: 0)
  --verify {False,True}
                        Verify SSL certificate on server side. True as default (default: True)
  -v, --version         show program's version number and exit

environment variables:
    HTTP_AUTHORIZATION - HTTP Authorization header
    X-API-KEY - HTTP X-API-KEY header

```



## Examples

### mllp2http

Run an HTTP debugging server:

```sh
docker run -p 8000:80 --rm kennethreitz/httpbin
```

Run the MLLP connector:

```sh
mllp2http https://localhost:8000
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
