import logging
from flask import Flask
from flask_restful import Resource, Api
from waitress import serve
from Shared.Database import Database_Loader, Database_Updater
from Shared.Services.DataLoader import Data_Loader
from Web.Controller.HomeController import HomeController
from Web.Controller.UploadController import UploadController
from Web.Controller.ToolController import ToolController
from Web.Controller.ComponentsController import ComponentsController
from Web.Controller.ToolDetailController import ToolDetailController
from Web.Controller.AuthenticationController import AuthenticationController

app = Flask(__name__, template_folder="../Web/templates")
api = Api(app)


def start():
    """
    Starts the web server. Entry point of the web application
    """
    logging.info("Starting the HIPA tool in web server mode...")
    Database_Loader.connect_db()
    Database_Updater.update_db()
    Data_Loader.load_folders()
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
    api.add_resource(ToolDetailController, '/tool/detail/<evaluation_folder>')
    api.add_resource(ComponentsController, '/components/<component>')
    api.add_resource(AuthenticationController, '/authentication/<sub_route>')
