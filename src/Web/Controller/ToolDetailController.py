from flask_restful import Resource
from flask import Flask, escape, request, jsonify, request, render_template, make_response
from Shared.Classes.Folder import Folder
from Shared.Services.DataLoader import Data_Loader


class ToolDetailController(Resource):
    def get(self, evaluation_folder: str):
        try:
            # TODO: Implement find function
            folder: Folder = Data_Loader.find_evaluation_folder(evaluation_folder)

            if folder is None:
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template('home.html'), 200, headers)

            print(f"folder found {folder.name}")
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('tool-detail.html', folder=folder), 200, headers)

        except BaseException as ex:
            print(ex)
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('home.html'), 200, headers)
