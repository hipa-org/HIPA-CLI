from flask_restful import Resource
from flask import Flask, escape, request, jsonify, request, render_template, make_response


class ComponentsController(Resource):
    def get(self, component: str):
        if component == "navbar":
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('navbar.html'), 200, headers)
