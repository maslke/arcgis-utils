import json
import os
from ags import create_user

"""
    Create Enterprise GeoDatabase
"""


def handle(request):
    content_length = int(request.headers['Content-Length'])
    post_data = request.rfile.read(content_length)
    if post_data is None:
        message = 'request parameter is empty'
        print message
        request.send_response(200)
        request.send_header('Content-type', 'text/plain')
        request.end_headers()
        request.wfile.write(message)
        exit()
    try:
        request_data = json.loads(post_data)
    except ValueError:
        message = 'invalid json format:{}, exit'.format(post_data)
        print message
        request.send_response(400)
        request.send_header('Content-type', 'text/plain')
        request.end_headers()
        request.wfile.write(message)
        exit()
    request_data['authorization_file'] = request.authorization_file
    messages = create_user.create(request_data)
    request.send_response(200)
    request.send_header('Content-type', 'text/plain')
    request.end_headers()
    request.wfile.write(os.linesep.join(messages))