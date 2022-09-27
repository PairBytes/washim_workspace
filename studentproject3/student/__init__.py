from flask import Flask, make_response, json, g, request, jsonify, redirect
from flask_restful import Resource, Api, reqparse
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import config
import time
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from student.helper.mongo_base import Base_Mongo
# from pymongo import MongoClient


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)
ma = Marshmallow(app)

# mongo_client = MongoClient(
#     host=app.config['localhost'], port=int(app.config['27017']), username=app.config['MONGO_USER'],
#     password=app.config['1234'], authSource=app.config['MONGO_AUTHSOURCE'])
# student_mongo_db = mongo_client[app.config['MONGO_DATABASE']]

migrate = Migrate(app, db)



if app.config['DEBUG']:
    app.debug = True

import student.routes.routes

@app.before_request
def start_timer():
    g.start = time.time()

@app.before_first_request
def create_table():
    db.create_all()

from flask import request, jsonify




@api.representation('application/json')
def output_json(data, code, headers=None):
    if code == 400 or code == 401:
        data['status'] = 0
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp


def conf_logging(app):
    """
    Setup proper logging
    """

    if app.debug is True:
        from student.student_file_handler import HelloFileHandler
        import logging
        file_handler = HelloFileHandler(app.config['LOG_FILE'],
                                                   maxBytes=1024 * 1024 * 100,
                                                   backupCount=31)
        if app.config['LOG_LEVEL'] == 'INFO':
            file_handler.setLevel(logging.INFO)
        elif app.config['LOG_LEVEL'] == 'DEBUG':
            file_handler.setLevel(logging.DEBUG)
        elif app.config['LOG_LEVEL'] == 'WARNING':
            file_handler.setLevel(logging.WARNING)
        else:
            file_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(file_handler.level)


conf_logging(app)


UPLOAD_FOLDER = 'D:/workspace/washim_workspace/Upload'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024