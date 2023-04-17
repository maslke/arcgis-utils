import arcpy
import uuid
import tempfile
import os


def save_as(input_mxd_name, extension='.mxd', version='10.3'):
    tmp_dir = tempfile.gettempdir()
    input_mxd = os.path.join(tmp_dir, input_mxd_name)
    mxd = arcpy.mapping.MapDocument(input_mxd)
    output_mxd = os.path.join(tmp_dir, uuid.uuid4().hex + extension)
    try:
        mxd.saveACopy(output_mxd, version)
    except arcpy.ExecuteError:
        print 'fail to convert mxd version'
        return None
    return output_mxd
