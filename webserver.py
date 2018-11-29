#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

from classification import predict_simple as predict
import glob 
import sys 

    
class PredictionServer(BaseHTTPRequestHandler):    
    @staticmethod
    def _predict():    
        results = []
        for file in glob.glob('input/*.jpg'):
            results.append(map(str, predict(file)))
            
        return results
        
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><pre>")
        
        for result in PredictionServer._predict():
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
    print PredictionServer._predict()
    