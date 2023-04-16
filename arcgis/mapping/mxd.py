import arcpy
import uuid


def save_as(input_mxd, version = '10.3'):
    mxd = arcpy.mapping.MapDocument(input_mxd)
    output_mxd = './mxds/' + uuid.uuid4().hex + '.mxd'
    mxd.saveACopy(output_mxd, version)
