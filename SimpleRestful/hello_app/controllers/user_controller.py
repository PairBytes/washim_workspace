from unicodedata import name
import urllib.request
from hello_app.decorators.authenticated import authenticated
from flask_restful import Resource, reqparse
from hello_app.helper.rest_response import RestResponse
from hello_app import app
from hello_app.services.user_service import UserService

from flask import request

class Users(Resource):

    @authenticated()
    def get(self, current_user_id, user_id=None):
        try:
            app.logger.info("Users:get:current_user_id:{}".format(current_user_id))
            if user_id is None:
                return UserService().get_user(current_user_id)
            elif int(current_user_id) == int(user_id):
                return UserService().get_user(user_id)
            else:
                return RestResponse(err='Unauthorized User !!').to_json(), 401
        except Exception as e:
            app.logger.error("Users:get:error:{}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500
    
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Name can not be blank', required=True)
            parser.add_argument('password', type=str, help='Password can not be blank', required=True)
            parser.add_argument('user_type', type=str, help='user_type can not be blank', required=True)
            parser.add_argument('department_type', type=str)

            args = parser.parse_args()
            app.logger.debug("Users:CustomLogin::post::params::{}".format(args))

            return UserService().custom_login(args['email'], args['password'], args['user_type'],
                                              args['department_type'])

        except Exception as e:
            app.logger.error("Users:CustomLogin:post::error:{}".format(e))
            return RestResponse(err='Something went wrong').to_json(), 500
    
class CustomSignup(Resource):

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Name can not be blank', required=True)
            parser.add_argument('password', type=str, help='Password can not be blank', required=True)
            parser.add_argument('user_type', type=str, help='user_type can not be blank', required=True)
            parser.add_argument('first_name', type=str)
            parser.add_argument('last_name', type=str)
            parser.add_argument('country_code', type=str)
            parser.add_argument('mobile_number', type=str)
            parser.add_argument('department_type', type=str)

            args = parser.parse_args()
            app.logger.debug("Users:CustomSignup:post:payload:{}".format(args))

            return UserService().custom_signup(args['email'], args['password'], args['user_type'], args['first_name'],
                                                args['last_name'], args['country_code'], args['mobile_number'],
                                                args['department_type'])
        except Exception as e:
            app.logger.error("User:CustomSignup:post:error:{}".format(e))
            return RestResponse(err='Something went wrong').to_json(), 500

class ValidateEmailOTP(Resource):

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email can not be blank', required=True)
            parser.add_argument('otp', type=str, help='OTP can not be blank', required=True)
            parser.add_argument('user_type', type=str, help='UserType can not be blank', required=True)

            args = parser.parse_args()
            app.logger.debug("Users:ValidateEmailOTP::post::params::{}".format(args))

            return UserService().validate_otp_email(args['email'], args['user_type'], args['otp'])

        except Exception as e:
            app.logger.error("ValidateEmailOTP::post::error:{}".format(e))
            return RestResponse(err='Something went wrong').to_json(), 500