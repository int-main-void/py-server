#!/usr/bin/env python
#
# server.py - very simple python webserver. It could serve as a starting point for a REST service.
#           - note that CORS is disabled for all clients in this version.
#           - currently it only accepts JSON Post requests, and echos back the body.
#

import BaseHTTPServer
import json
import logging
import logging.handlers
import os

HOST_KEY='HOST'
PORT_KEY='PORT'
DEFAULT_HOST=''
DEFAULT_PORT=9080
LOG_FILENAME='/opt/app/log/server.log'

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()

    # enable CORS - may not be desireable...
    def do_OPTIONS(s):
        s.send_response(200)
        s.send_header('Access-Control-Allow-Origin', '*')
        s.send_header('Access-Control-Allow-Methods', 'POST, GET')
        s.send_header('Access-Control-Allow-Headers', 'Content-Type,Accept')
        s.end_headers()

    def do_POST(s):
        logging.info('%s request received for %s from %s' % (s.command, s.path, s.client_address))

        if(s.headers['content-type'] != 'application/json'):
            logging.debug('invalid header %s' % s.headers['content-type'])
            s.send_response(400)
            return

        body = "{}"
        if('Content-Length' in s.headers):
            length = int(s.headers['Content-Length'])
            body = s.rfile.read(length)

        payload = {}
        try:
            payload = json.loads(body)
        except Exception as e:
            logging.debug('unable to parse request body as json')
            s.send_response(400)

        s.send_response(200)
        s.send_header('Access-Control-Allow-Origin', '*') # allow CORS...
        s.send_header('Content-Type', 'application/json')
        s.end_headers()
        s.wfile.write(payload) # echo back request
        return
            

def run(host, port,
        server_class=BaseHTTPServer.HTTPServer,
        handler_class=HTTPHandler):
    server_address=(host,port)
    httpd=server_class(server_address, handler_class)
    logging.info("Server starting - %s:%s" % (host, port))
    httpd.serve_forever()
    

def main():
    logging.basicConfig(format='%(asctime)s:SERVER:[%(levelname)s]:%(message)s',
                        level=logging.DEBUG)
    # uncomment these lines to log to a file
    #loghandler=logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=2000000, backupCount=5)
    #logging.getLogger().addHandler(loghandler)

    host = os.getenv(HOST_KEY, DEFAULT_HOST)
    port = int(os.getenv(PORT_KEY, DEFAULT_PORT))
    run(host, port)

main()
