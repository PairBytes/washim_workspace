from importlib.metadata import files
from flask_restful import Resource, reqparse
from student import app
import student
from student.services.student_service import StudentService
from student.helper.rest_response import RestResponse
from student.decorators.authenticated import authenticated, emb_authenticated
from flask import g, request

import werkzeug

class CustomSignup(Resource):
        def post(self):
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

            print('Email;',args['email'] ,'Password:',args['password'],'User Type:',args['user_type'],'first Name:',args['first_name'],
                                               'Last Name',args['last_name'],'country code:',args['country_code'],'Mobile No.:',args['mobile_number'],
                                               'Department:',args['department_type'])

            return StudentService().custom_signup(args['email'], args['password'], args['user_type'], args['first_name'],
                                                args['last_name'], args['country_code'], args['mobile_number'],
                                                args['department_type'])


class ValidateEmailOTP(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='Email can not be blank', required=True)
        parser.add_argument('otp', type=str, help='OTP can not be blank', required=True)
        parser.add_argument('user_type', type=str, help='UserType can not be blank', required=True)

        args = parser.parse_args()
        app.logger.debug("Users:ValidateEmailOTP::post::params::{}".format(args))
        print('Email:',args['email'],'User_Type:',args['user_type'],'OTP', args['otp'])

        return StudentService().validate_otp_email(args['email'], args['user_type'], args['otp'])

class Student(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='Name can not be blank', required=True)
        parser.add_argument('password', type=str, help='Password can not be blank', required=True)
        parser.add_argument('user_type', type=str, help='user_type can not be blank', required=True)
        parser.add_argument('department_type', type=str)

        args = parser.parse_args()
        app.logger.debug("Users:CustomLogin::post::params::{}".format(args))

        print('Email:',args['email'],'Password:',args['password'],'User Type:',args['user_type'],'Department:',args['department_type'])

        return StudentService().custom_login(args['email'], args['password'], args['user_type'],
                                            args['department_type'])

    @authenticated()
    def get(self, current_user_id, user_id=None):
        app.logger.info("Users:get:current_user_id:{}".format(current_user_id))
        if user_id is None:
            return StudentService().get_user(current_user_id)
        elif int(current_user_id) == int(user_id):
            return StudentService().get_user(user_id)
        else:
            return RestResponse(err='Unauthorized User !!').to_json(), 401

    @authenticated()
    def put(self, current_user_id):

        parser = reqparse.RequestParser()
        parser.add_argument('data', type=dict, help='User data can not be blank', required=True)
        args = parser.parse_args()
        print("args...", args)
        app.logger.info("Users::put::request_body::{}".format(args))

        app.logger.info("Users:CustomLogin::put:user_id:{}".format(current_user_id))
        return StudentService().update_user(current_user_id, args['data'])


class ForgotPassword(Resource):
    print('Resorce:', Resource)
    def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email can not be blank', required=True)
            args = parser.parse_args()
            app.logger.debug("Users:ForgotPassword::post::body::{}".format(args))
            return StudentService().forgot_password(args['email'])
     
class ResetPassword(Resource):

    def post(self):
        # try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Code can not be blank', required=True)
            parser.add_argument('password', type=str, help='Password can not be blank', required=True)
          
            args = parser.parse_args()
            app.logger.debug("Users:ResetPassword::post::body::{}".format(args))

            if args['password'] == '':
                return RestResponse(err='Password can not be blank').to_json(), 400
            # if not args['code']:
            #     return RestResponse(err='Code can not be blank').to_json(), 400
            return StudentService().reset_password(args['email'],args['password'])
        # except Exception as e:
        #     app.logger.error("ResetPassword::post:error:{}".format(e))
        #     return RestResponse(err='Something went wrong').to_json(), 500


class CustomSigout(Resource):
    @authenticated()
    def post(self, current_user_id, user_id=None):
        app.logger.info("Users:post:current_user_id:{}".format(current_user_id))
        print('current_userid:',current_user_id)
        if user_id is None:
            print('Sudent.singout user:',StudentService().signout_user(current_user_id))
            return StudentService().signout_user(current_user_id)
        elif int(current_user_id) == int(user_id):
            print('Sudent.singout user:',StudentService().signout_user(user_id))
            return StudentService().signout_user(user_id)
        else:
            return RestResponse(err='Unauthorized User !!').to_json(), 401


    # # def post(self, current_user_id):
    #     user = StudentModel.find_by_id(current_user_id)
    #     print('User_Id:')
    #     return 'SignOut Page'
        # user = StudentModel.find_by_id(current_user_id)
        # user.authenticated = False
        # db.session.add(self)
        # db.session.commit()
        # db.save()
        # logout_user()
        # return jsonify({'success': True})



    # def post(self):

    #     jti = get_raw_jwt()['jti']

    #     try:
    #         # Revoking access token
    #         revoked_token = RevokedTokenModel(jti=jti)

    #         revoked_token.add()

    #         return {'message': 'Access token has been revoked'}

    #     except:

    #         return {'message': 'Something went wrong'}, 500
    # def post(self):
        # get auth token
       
    # def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        print('Auth_Header:',auth_header)
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = StudentModel.to_json_access_token(auth_token)
            print('Resp:',resp)
            
            
            # insert the token
            db.session.add(resp)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            return RestResponse(student, status=1).to_json(), 200
        

class UserSearch(Resource):
    @emb_authenticated()
    def get(self, current_user_id, user_type=None):
        # try:
            app.logger.info("Users:UserSearch:get:user_id:{}".format(current_user_id))
            parser = reqparse.RequestParser()
            print('parser:',parser)
            parser.add_argument('query', type=str, help='Query can not be blank', required=True)
            parser.add_argument('page', type=int, default=1)
            parser.add_argument('limit', type=int, default=10)
            args = parser.parse_args()
            app.logger.debug("Users:UserSearch::get::params::{}".format(args))
            if not args['query']:
                return RestResponse([], err='Query can not be blank').to_json(), 400
            if not type:
                return RestResponse([], err='UserType can not be blank').to_json(), 400
            print('Current User Id:',current_user_id,'User Type', user_type.strip(),'Query:', args['query'].strip(), 'Page:', args['page'],'Limit',
                                             args['limit'])
            return StudentService().user_search(current_user_id, user_type.strip(), args['query'].strip(), args['page'],
                                             args['limit'])
        # except Exception as e:
        #     app.logger.error("Users:UserSearch::get:error:{}".format(str(e)))
        #     return RestResponse([], err=str(e)).to_json(), 500



class UploadUserProfile(Resource):
    @authenticated()
    def post(self, current_user_id):
        # try:
            app.logger.info("UploadUserProfile::Post:user_id: {}".format(current_user_id))
            parser = reqparse.RequestParser()
            print('hello::::::::::::::::::')
            parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True)
            # parser.add_argument('upload_type', type=str, help='Upload Type can not be blank')
            args = parser.parse_args()
            print('Args:',args)
            
            app.logger.debug("UploadUserProfile:post:body::{}".format(args))
            # if not args['upload_type']:
            #     return RestResponse(err='Upload Type can not be blank').to_json(), 400
            print('File Upload Data:',args['file'], current_user_id)
            return StudentService().upload_file(args['file'], current_user_id)
        # except Exception as e:
        #     app.logger.error("UploadUserProfile:post:error:{}".format(e))
        #     return RestResponse(err='Something went wrong').to_json(), 500
