from flask_restful import Resource, reqparse
from flask import request
from werkzeug.utils import secure_filename
from pathlib import Path
from Shared.Services.Config.Configuration import Config

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadController(Resource):
    def post(self):
        print(request)
        uploaded_files = request.files.getlist("files")
        print(uploaded_files)
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(Path.joinpath(Config.DATA_RAW_DIRECTORY, filename))
        pass
