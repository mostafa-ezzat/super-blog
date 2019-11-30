from werkzeug.datastructures import FileStorage
from flask_restplus import reqparse

jpeg_upload = reqparse.RequestParser()
jpeg_upload.add_argument('thumbnail', type=FileStorage, location='files',
                         required=True, help='JPEG File')
