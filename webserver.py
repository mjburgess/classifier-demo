#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

import classification
import glob 

PREDICTOR = predict_simple

class Server(BaseHTTPRequestHandler):    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><pre>")
        
        for prediction in map(PREDICTOR, glob.glob('input/*.jpg')):
            self.wfile.write(prediction)
        
        self.wfile.write("</pre></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        return self.do_GET()
        
server_address = ('', 80)
httpd = HTTPServer(server_address, Server)

print 'Starting httpd...'
httpd.serve_forever()

    