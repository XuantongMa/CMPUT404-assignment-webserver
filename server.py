#  coding: utf-8 
import socketserver
import os.path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def css_file(self, path):
        file = open( "./www"+ path,'r').read()
        status_code = "HTTP/1.1 200 OK\r\n"
        content_type = "Content-Type: text/css;\r\n"
        length = str(len(file))
        content_length = "Content-Length: {}\r\n".format(length)
        connection = "Connection : close\r\n"
        respond = status_code + content_type + content_length  + connection + file
        #print("111111111111111111111111111111111111111111")
        return respond
    
    def html_file(self, path):
        file = open( "./www"+ path,'r').read()
        status_code = "HTTP/1.1 200 OK\r\n"
        content_type = "Content-Type: text/html;\r\n"
        length = str(len(file))
        content_length = "Content-Length: {}\r\n".format(length)
        connection = "Connection : close \r\n"
        respond = status_code + content_type + content_length + connection + file
        #print("222222222222222222222222222222222222222222")
        return respond

    def index_file1(self, path):
        path = f"./www{path}index.html"
        if open( path,'r').read():
            file = open( path,'r').read()
            status_code = "HTTP/1.1 200 OK\r\n"
            content_type = "Content-Type: text/html;\r\n"
            length = str(len(file))
            content_length = ("Content-Length: {}\r\n".format(length))
            connection = "Connection : close \r\n"
            respond = status_code + content_type + content_length + connection + file
            #print("333333333333333333333333333333333333333333")                         
        else:
            respond = "HTTP/1.1 404 Not Found"
            #print("4444444444444444444444444444444444444444")
        return respond

    def index_file2(self, path):
        if os.path.isfile("./www{}/index.html".format(path)):
            status_code = "HTTP/1.1 301 Moved Permanently"
            location= "Location: http://127.0.0.1:8080{}/".format(path)
            respond = "{0}\r\n{1}\r\n{2}".format(status_code, location, "\r\n")
            #print("55555555555555555555555555555555555555")
        else:
            respond = "HTTP/1.1 404 Not Found"
            #print("666666666666666666666666666666666666666666")
        return respond

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        request = self.data.decode().split()
        method = request[0]
        path = request[1]
        if method != "GET":
            respond = "HTTP/1.1 405 Method Not Allowed"
            #print("777777777777777777777777777777777777")
        else:
            check = os.path.realpath(f"./www/{path}").startswith(os.path.realpath("./www"))
            if check == False:
                respond = "HTTP/1.1 404 Not Found"
                #print("88888888888888888888888888888888888")   
            else:
                if os.path.exists("./www{}".format(path)) and path.endswith("css"):
                        respond = self.css_file(path)
                elif os.path.exists("./www{}".format(path)) and path.endswith("html"):
                        respond = self.html_file(path)                          
                elif os.path.exists("./www{}/index.html".format(path)) and path.endswith("/"):
                        respond = self.index_file1(path)
                else:
                        respond = self.index_file2(path)
        self.request.sendall(respond.encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
