from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import json
import create_user
import os
import functools

"""
    HELP CONTENTS
"""
def get_help():
    return """
        #########################
        end-point: /help
        method: 'GET'
        #########################
        end-point: /create_user
        for: Create Enterprise Geodatabase
        method: 'POST'
        how to use:
            1. PostgreSQL
            curl --location 'http://localhost:10000/create_user' \
                    --header 'Content-Type: text/plain' \
                        --data '{
                        "database_platform":"PostgreSQL",
                        "instance_name":"",
                        "database_name":"",
                        "database_admin":"",
                        "database_admin_password":"",
                        "gdb_admin_name":"",
                        "gdb_admin_password":""}
            2. Oracle
            curl --location 'http://localhost:10000/create_user' \
                    --header 'Content-Type: text/plain' \
                        --data '{
                        "database_platform":"Oracle",
                        "instance_name":"",
                        "database_admin":"",
                        "database_admin_password":"",
                        "gdb_admin_name":"",
                        "gdb_admin_password":""}
        #########################
    """


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server, authorization_file = None):
        self.authorization_file = authorization_file
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        parsed_data = urlparse.urlparse(self.path)
        request_path = parsed_data.path
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        if request_path == '/help':
            self.wfile.write(get_help())
        else:
            self.wfile.write("no handler for request path:{}".format(request_path))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = urlparse.urlparse(self.path)
        request_path = parsed_data.path
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        if post_data is None:
            message = 'request parameter is empty'
            print message
            self.wfile.write(message)
            exit()
        try:
            request_data = json.loads(post_data)
        except ValueError:
            message = 'invalid json format:{}, exit'.format(post_data)
            print message
            self.wfile.write(message)
            exit()
        if request_path == '/create_user':
            request_data['authorization_file'] = self.authorization_file
            messages = create_user.create(request_data)
            self.wfile.write(os.linesep.join(messages))
        else:
            self.wfile.write("no handler for request path:{}".format(request_path))


def run(authorization_file, server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    handler_partial = functools.partial(handler_class, authorization_file=authorization_file)
    httpd = server_class(server_address, handler_partial)
    print 'Starting httpd on port {}'.format(port)
    httpd.serve_forever()
