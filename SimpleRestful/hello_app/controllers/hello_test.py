from flask_restful import Resource, reqparse
from hello_app import app

class HelloTest(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            args = parser.parse_args()
            return args

        except Exception as e:
            app.logger.error("HelloTest:get:error:{}".format(str(e)))