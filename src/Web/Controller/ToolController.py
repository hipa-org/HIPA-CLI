from flask_restful import Resource
from flask import make_response, render_template


class ToolController(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('tool.html'), 200, headers)
