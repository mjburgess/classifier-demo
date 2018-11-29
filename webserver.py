#!/usr/bin/env python

from classification import predict_simple as predict

"""
To use the ResNet50 pre-trained CNN
    pip install keras tensorflow pillow
    
and then uncomment the following import...
"""

# from classification import predict_neural as predict

import glob 
import sys 
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
    
class PredictionServer(BaseHTTPRequestHandler):  
    TEMPLATE = 'template.html'
    
    @staticmethod
    def _predict():    
        results = []
        for file in glob.glob('input/*.jpg'):
            for guess in predict(file):
                results.append(str(guess))
            
        return results
        
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        
        self.wfile.write(
            open(PredictionServer.TEMPLATE).read().format(
                predictions='\n'.join(PredictionServer._predict())
            )
        )

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        return self.do_GET()
        
            

if len(sys.argv) > 1:
    server_address = ('', 80)
    httpd = HTTPServer(server_address, PredictionServer)

    print 'Starting httpd...'
    httpd.serve_forever()
else:
    print "Predictions for images in input/"
    for guess in PredictionServer._predict():
		print guess
    