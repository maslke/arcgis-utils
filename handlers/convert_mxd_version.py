import cgi
import uuid


def handle(request):
    content_type = request.headers['Content-Type']
    if content_type.startswith('multipart/form-data'):
        form = cgi.FieldStorage(fp=request.rfile, headers=request.headers, environ={'REQUEST_METHOD': 'POST'})
        if 'mxd' in form.keys():
            field_item = form['mxd']
            if field_item.filename:
                new_name = uuid.uuid4().hex + '-' + field_item.filename
                with open('./mxds/' + new_name, 'wb') as f:
                    f.write(field_item.file.read())

            else:
                request.send_response(400)
                request.send_header('Content-type', 'text/plain')
                request.end_headers()
                request.wfile.write('no uploaded mxd file')
        else:
            request.send_response(400)
            request.send_header('Content-type', 'text/plain')
            request.end_headers()
            request.wfile.write('no uploaded mxd file')