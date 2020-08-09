from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from flask import request


class UploadController(Resource):
    def post(self):
        print(request)
        uploaded_files = request.files.getlist("files")
        print(uploaded_files)
        pass
