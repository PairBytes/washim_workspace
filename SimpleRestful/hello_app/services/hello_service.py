from flask_restful import Resource


class HelloService(Resource):
    @staticmethod
    def get_username(username):
        print('User Name: ',username)
        return username



