import logging
from flask import Flask
from flask_restful import Resource, Api
from waitress import serve
from Web.Controller.HomeController import HomeController
from Web.Controller.UploadController import UploadController
from Web.Controller.ToolController import ToolController
from Web.Controller.ComponentsController import ComponentsController

app = Flask(__name__, template_folder="../Web/templates")
api = Api(app)


def start():
    """
    Starts the web server. Entry point of the web application
    """
    logging.info("Starting the HIPA tool in web server mode...")
    load_api()
    serve(app, host='0.0.0.0', port=15000, threads=16)


def load_api():
    """
    Loads all api routes
    """
    logging.info("Loading api controllers...")
    api.add_resource(HomeController, '/')
    api.add_resource(UploadController, '/upload')
    api.add_resource(ToolController, '/tool')
    api.add_resource(ComponentsController, '/components/<component>')
