from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
from handlers import convert_mxd_version, create_user_handler
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
        end-point: /management/create_user
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
            curl --location 'http://localhost:10000/management/create_user' \
                    --header 'Content-Type: text/plain' \
                        --data '{
                        "database_platform":"Oracle",
                        "instance_name":"",
                        "database_admin":"",
                        "database_admin_password":"",
                        "gdb_admin_name":"",
                        "gdb_admin_password":""}
        #########################
        end-point: /mapping/convert_mxd_version
        for: Change mxd version to a lower one
        method: 'POST'
        how to use:
            Content-Type: multipart/form-data
            body: form-data
            key1: file(upload the mxd file)
            key2: version(if none,default is 10.3)
        #########################
    """


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server, authorization_file=None):
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
        parsed_data = urlparse.urlparse(self.path)
        request_path = parsed_data.path

        if request_path == 'management/create_user':
            create_user_handler.handle(self)
        elif request_path == '/mapping/convert-mxd-version':
            convert_mxd_version.handle(self)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("no handler for request path:{}".format(request_path))


def run(authorization_file, server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    handler_partial = functools.partial(handler_class, authorization_file=authorization_file)
    httpd = server_class(server_address, handler_partial)
    print 'Starting httpd on port {}'.format(port)
    httpd.serve_forever()


if __name__ == '__main__':
    run(authorization_file='')

