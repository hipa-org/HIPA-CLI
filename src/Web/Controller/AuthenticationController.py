from flask_restful import Resource
from flask import Flask, escape, request, jsonify, request, render_template, make_response, redirect


class ComponentsController(Resource):
    def get(self, sub_route: str):

        if sub_route == 'signup':
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('signup.html'), 200, headers)

        if sub_route == "signin":
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('signin.html'), 200, headers)

        if sub_route == 'signout':
            return redirect("/home", code=302)
