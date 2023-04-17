import cgi
import tempfile
import os

from arcgis.mapping import mxd

"""
    CHANGE MXD FILE VERSION
    MUST BE CHANGE TO LOWER VERSION
"""
def handle(request):
    content_type = request.headers['Content-Type']
    extension = '.mxd'
    if content_type.startswith('multipart/form-data'):
        form = cgi.FieldStorage(fp=request.rfile, headers=request.headers, environ={'REQUEST_METHOD': 'POST'})
        version = form['version']
        if 'file' in form.keys():
            field_item = form['mxd']
            if field_item.filename:
                file_name = field_item.filename
                if file_name[-len(extension):].lower() != extension:
                    request.send_response(400)
                    request.send_header('Content-type', 'text/plain')
                    request.end_headers()
                    request.wfile.write('no uploaded mxd file')
                    return
                with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as tmp_file:
                    tmp_file.write(field_item.file.read())
                    output_mxd_file = mxd.save_as(tmp_file.name, extension, version)
                    request.send_response(200)
                    request.send_header('Content-type', 'application/octet-stream')
                    request.send_header('Content-Disposition', 'attachment; filename={}'.format(field_item.filename))
                    request.end_headers()
                    tmp_dir = tempfile.gettempdir()
                    file_path = os.path.join(tmp_dir, output_mxd_file)
                    with open(file_path, 'rb') as f:
                        request.wfile.write(f.read())

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