from flask_restful import Resource, reqparse
from flask import Flask, escape, request, jsonify, request, render_template, make_response, redirect
from werkzeug.utils import secure_filename
from pathlib import Path
from Shared.Services.Configuration import Configuration_Service
from Shared.Services.FileManagement import Folder_Management
import logging
from Shared.Classes.Folder import Folder
from Shared.Classes.File import File
from Web.RuntimeConstants import Folders

ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadController(Resource):
    def post(self):
        Config = Configuration_Service.get_config()
        uploaded_files = request.files.getlist("files")

        if Config.DEBUG:
            print(uploaded_files)

        try:
            # Create a new folder entity
            evaluation_folder: Folder = Folder()

            # Create a new directory
            Folder_Management.create_directory(Path.joinpath(Config.DATA_RAW_DIRECTORY, evaluation_folder.name))

            # Iterate through all uploaded files
            for file in uploaded_files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(Path.joinpath(Config.DATA_RAW_DIRECTORY, evaluation_folder.name, filename))
                    evaluation_folder.files.append(File(filename))

            # Add the folder to the global exposed array
            Folders.folders.append(evaluation_folder)

            return redirect(f'/tool/detail/{evaluation_folder.name}', code=302)

        except PermissionError as ex:
            logging.warning(ex)
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('home.html'), 200, headers)


        except BaseException as ex:
            logging.warning(ex)
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('home.html'), 200, headers)
