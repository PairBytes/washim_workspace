from flask import Flask, make_response, json, g, request, jsonify, redirect
from flask_restful import Resource, Api, reqparse
from flask_marshmallow import Marshmallow
import config
import time


app = Flask(__name__)
app.config.from_object('config')


api = Api(app)
ma = Marshmallow(app)


if app.config['DEBUG']:
    app.debug = True

@app.before_request
def start_timer():
    g.start = time.time()



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