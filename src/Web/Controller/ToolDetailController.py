from flask_restful import Resource
from flask import Flask, escape, request, jsonify, request, render_template, make_response
from Shared.Classes.Folder import Folder


class ToolDetailController(Resource):
    def get(self, evaluation_folder: str):
        try:
            # TODO: Implement find function
            folder: Folder = None

            if folder is None:
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template('home.html'), 200, headers)

            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('tool-detail.html'), 200, headers)

        except BaseException as ex:
            print(ex)
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('home.html'), 200, headers)
