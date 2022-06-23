from hello_app import api, app
# from flask import Blueprint

from hello_app.controllers.hello_test import *
from hello_app.Token.Token_Create import login
from hello_app.controllers.user_controller import CustomSignup, ValidateEmailOTP, Users



# api.add_resource(HelloTest,"/")
api.add_resource(BooksView, '/books')
api.add_resource(BookView,'/books/<string:name>')
app.add_url_rule('/login','login',login)
api.add_resource(CustomSignup, '/api/v1/user/signup')
api.add_resource(ValidateEmailOTP, '/api/v1/validate_email/otp')
api.add_resource(Users, '/api/v1/user', '/api/v1/user/<user_id>')