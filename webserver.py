#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

import classification
import glob 
import sys 

RESULTS = []
for file in glob.glob('input/*.jpg'):
    RESULTS.append(
        map(str, classification.predict_simple(file))
    )

    
class Server(BaseHTTPRequestHandler):    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><pre>")
        
        for result in RESULTS:
            self.wfile.write(result)
            
        self.wfile.write("</pre></body></html>")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        return self.do_GET()
        
            

if len(sys.argv) > 1:
    server_address = ('', 80)
    httpd = HTTPServer(server_address, Server)

    print 'Starting httpd...'
    httpd.serve_forever()
else:
    print RESULTS
    