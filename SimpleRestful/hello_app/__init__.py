from flask import Flask, make_response, json, g, request, jsonify, redirect
from flask_restful import Resource, Api, reqparse
from flask_marshmallow import Marshmallow
import config
import time
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

api = Api(app)
# db.init_app(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)



if app.config['DEBUG']:
    app.debug = True

import hello_app.routes.routes

@app.before_request
def start_timer():
    g.start = time.time()

@app.before_first_request
def create_table():
    db.create_all()

from flask import request, jsonify
import jwt

from functools import wraps
def  token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message':'Token is Missing!'}),403
        try:
            data = jwt.decode(token, 'SECRET_KEY',algorithms=['HS256'])
        except:
            return jsonify({'message':'Token is Invalid!'})
        return f(*args, **kwargs)
    
    return decorated



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
        from hello_app.hello_file_handler import HelloFileHandler
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
