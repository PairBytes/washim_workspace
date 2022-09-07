from cgi import print_directory
import email
import imp
from itertools import count
from os import access
from time import process_time_ns
from turtle import update
from wsgiref.util import request_uri
import student
from student.models.student_model import StudentModel
from student.models.std_verification_model import StdVerificationModel
from student.helper.rest_response import RestResponse
import uuid
from datetime import datetime, date, timedelta
import random
from student import app, db
from flask_jwt_extended import create_access_token
from student.helper.auth_utils import generate_jwt_token
from student.helper.mongo_base import Base_Mongo
from flask import g, request
from student.helper.auth_utils import generate_jwt_token, decode_jwt_token


class StudentService:
    # def __init__(self):
    #     self.user_validate_coll = Base_Mongo(student_mongo_db, app.config['USR_VALIDATE_COLL'])

    def custom_signup(self, email, password, user_type, first_name, last_name, country_code, mobile_number,
                      department_type):
            student = StudentModel.find_by_email(email)
            print('Student:',student)
            if not student:
                if country_code and mobile_number:
                    if StudentModel.find_by_mobile(country_code.strip(), mobile_number.strip()):
                        return RestResponse(err="Mobile Number already exists.").to_json(), 400
                elif country_code and not mobile_number:
                    return RestResponse(err="Mobile Number can not be blank.").to_json(), 400
                elif not country_code and mobile_number:
                    return RestResponse(err="Country Code can not be blank.").to_json(), 400

                if self.generate_otp_email(email, user_type):
                    password = StudentModel.generate_password_hash(password)
                    print('password:',password)
                    user_uuid = str(uuid.uuid4())
                    print('User_id:',user_uuid)
                    student = StudentModel(email=email, password=password, user_type=user_type, first_name=first_name,
                                      last_name=last_name, country_code=country_code, mobile_number=mobile_number,
                                      signup_type='email', userid=user_uuid, created_at=datetime.utcnow(),
                                      updated_at=datetime.utcnow(), department_type=department_type
                                      )
                    print('Student:',student)
                    student.temp_save()
                    student.created_by = student.updated_by = student.id
                    print('Studnt.created_by:',student.created_by)
                    student.save()
                    return RestResponse(
                        {'email': email, 'user_type': user_type}, message='OTP has been sent to your email address',
                        status=1).to_json(), 201
                else:
                    return RestResponse(err='Error while sending mail for verification').to_json(), 500
            else:
                return RestResponse(err="User already exists!").to_json(), 403

    def generate_otp_email(self, email, user_type=None):

        otp = ""
        for i in range(4):
            otp += str(random.randint(0, 9))

        std_verify = StdVerificationModel(usr_type=user_type, verification_id=email, otp=otp, is_expired=False,
                                            verification_type='email', otp_time=datetime.utcnow(), attempts=0)
        print('Std_Verify:',std_verify)
        std_verify.save()
        html_body = """\
        <html>
        <head></head>
        <body> 
            <p> Verification Code <br> {} <br> Here is your Verification Code.</p>
        </body>
        </html>
        """.format(otp)

        # aws_mail_obj = AmazonSESMailSend(app.config['AWS_FROM_EMAIL_ADDR'])
        # is_send, msg = aws_mail_obj.send_mail('Email Verification', [email], html_message=html_body)
        std_verify.is_send = True
        std_verify.message = "msg"
        std_verify.save()
        print('Html_Body : ',html_body)
        return True
    
    def validate_otp_email(self, email, user_type, otp, user=None):
    
        std_verify = StdVerificationModel.query.order_by(StdVerificationModel.otp_time.desc()).filter_by(
            verification_id=email, usr_type=user_type).first()

        print('Std_verify:',std_verify)
        if std_verify:
            if std_verify.is_expired:
                app.logger.info("user verify data is expired ....{}.".format(str(std_verify.is_expired)))
                return RestResponse(err="OTP has been expired!").to_json(), 410
            elif otp.strip() == std_verify.otp:
                otp_time = int(
                    (datetime.utcnow() - std_verify.otp_time).total_seconds() / 60)
                print('OTP Time:',otp_time)
                app.logger.info("OTP Expire Now Time:{}".format(str(datetime.utcnow())))
                app.logger.info("OTP Time:{}".format(str(std_verify.otp_time)))
                app.logger.info("OTP Time min:{}".format(str(otp_time)))
                if otp_time > 15:
                    std_verify.is_expired = True
                    std_verify.save()
                    return RestResponse(err="OTP has been expired!").to_json(), 410
                else:
                    if user:
                        user.email_verify = True
                        user.email = email
                        print('user.email:',user.email)
                        
                    else:
                        user = StudentModel.find_by_email_and_usr_type(email, user_type)
                        print('User:',user)
                        user.email_verify = True
                        user.access_token = create_access_token(identity=str(user.userid), expires_delta=False)
                        print('Userid:',user.userid)
                        print('User.Access:',user.access_token)

                    user.save()

                    user = user.to_json()
                    return RestResponse(user, message="Email Validated", status=1).to_json(), 201
            else:
                return RestResponse(err='You entered invalid OTP.').to_json(), 400
        else:
            return RestResponse(err='Invalid Email Id.').to_json(), 400

    def get_user(self, user_id):
            app.logger.info("fetch user: {}".format(user_id))
  
            student = StudentModel.find_by_id(user_id)
            if student:
                student = student.to_json()
                return RestResponse(student, status=1).to_json(), 200
            else:
                return RestResponse(err='User not found!').to_json(), 400
    
    def custom_login(self, email, password, user_type, department_type):
        app.logger.info("custom login with email {}".format(email))

        user = StudentModel.find_by_email_and_usr_type(email, user_type)
        print('User:',user)
        if user:
            if not user.password:
                return RestResponse(err="Please set your password!").to_json(), 400
            if StudentModel.verify_hash(password, user.password):
                user.last_login = datetime.utcnow()
                user.last_login_type = 'email'
                if user.access_token is None or user.access_token == '':
                    user.access_token = create_access_token(identity=str(user.userid), expires_delta=False)
                user.save()
                user = user.to_json_access_token()
                print('user:',user)
                return RestResponse(user, message='You are logged in successfully', status=1).to_json(), 201
            else:
                return RestResponse(err="Invalid Password!").to_json(), 400
        else:
            return RestResponse(err="Email Id does not exist").to_json(), 400
      
    def update_user(self, user_id, data):

        user = StudentModel.find_by_id(user_id)
        is_update = False
        if user:
            columns = [col.name for col in user.__table__.columns if col.name != 'password']
            for u_data in data:
                if u_data in columns:
                    setattr(user, u_data, data[u_data])
                    is_update = True
            if is_update:
                user.updated_by = user.id
                user.updated_at = datetime.utcnow()
                user.save() 
        user = user.to_json()
        return RestResponse(user, message="Your profile has been updated successfully", status=1).to_json(), 200
    
    def forgot_password(self, email):
        # try:
            user = StudentModel.find_by_email(email)
            print('user:',user)
            if user:
                code = generate_jwt_token(email)
                user_validate = StudentModel.query.filter_by(
                    userid= str(user.id),
                    email= user.email,
                    user_type= user.user_type
                )
                
                print('User:',user)
                print('User_validate:::::::::::',user_validate)
                print('code:',code)
                # if user_validate:
                #     StudentModel.update(self,user=str(user.id),code=code)
                        
                # #             'code': code,
                                # code=code
                # #             'count': 0,
                # #             'updated_at': datetime.utcnow()
                # #         })
                # # else:
                # #     self.user_validate_coll.insert({
                # #         'user_id': str(user.id),
                # #         'email': user.email,
                # #         'code': code,
                # #         'is_expiry': False,
                # #         'count': 0,
                # #         'user_type': user.user_type,
                # #         'created_at': datetime.utcnow(),
                # #         'updated_at': datetime.utcnow()
                # #     })
                if user.user_type == 'student':
                    reset_url = """\
                        app.config['CLIENT_DASHBOARD_LINK'] + "/reset-password?code="+code"""
                    # reset_url='link'
                    print('Resest_url',reset_url)
                # else:
                #     reset_url = app.config['SUPPLY_DASHBOARD_LINK'] + "/reset-password?code=" + code

                if user.first_name and user.last_name:
                    user_name = user.first_name + ' ' + user.last_name
                elif user.first_name:
                    user_name = user.first_name
                else:
                    user_name = 'User'

                html_body = """\
                <html>
                <head></head>
                <body>
                    <p>Dear {},</p>
                    <p>
                        To reset your password
                        <a href={}>
                            click here
                        </a>.
                    </p>
                    <p>If you have not requested a password reset simply ignore this message.</p>
                    <p>Sincerely</p>
                    <p>ExMyB Support Team</p>
                </body>
                </html>
                """.format(user_name,reset_url)

    #             # # aws_mail_obj = AmazonSESMailSend(app.config['AWS_FROM_EMAIL_ADDR'])
    #             # # is_send, msg = aws_mail_obj.send_mail('[ExMyB] Reset Your Password', [user.email],
    #             # #                                       html_message=html_body)
    #             # # if is_send:
    #             # #     return RestResponse(message=msg, status=1).to_json(), 201
    #             # else:
    #             #     return RestResponse(err=msg).to_json(), 500
                print('HTML Body:', html_body)
            else:
                return RestResponse(err="Email Id does not exist").to_json(), 400
    #     except Exception as e:
    #         app.logger.error("UserService:forgot_pawword::error: {}".format(str(e)))
    #         return RestResponse(err=str(e)).to_json(), 500

    def reset_password(self, password, code):
    
            token = decode_jwt_token(code)
            print('Token:',token)
            if 'err' in token:
                return RestResponse(err="Invalid Token!").to_json(), 400
            if password:
                
                user = StudentModel.find_by_email(email=email)
                print('user:',user)
                if user:
                    password = StudentModel.generate_password_hash(password)
                    print('password:',password)
                    user.password = password
                    user.save()
                    return RestResponse(message='Password has been reset successfully', status=1).to_json(), 201

                else:
                    return RestResponse(err="user is not found!").to_json(), 400
        # except Exception as e:
        #     app.logger.error("UserService:reset_password::error: {}".format(str(e)))
        #     return RestResponse(err=str(e)).to_json(), 500


    def signout_user(self, user_id,):
        access_token = request.to_json.get("access_token")
        ref = StudentModel.query.filter_by(access_token=access_token).first()
        print('ref:',ref)
        print('access_token:',ref.access_token)
        # if ref is not None:
        #     return {"status": "already invalidated"}
        
        blacklist_refresh_token = StudentModel(access_token=ref.access_token)

        # Add refresh token to session.
        db.session.add(blacklist_refresh_token)

        # Commit session.
        db.session.commit()

        # Return status of refresh token.
        return {"status": "invalidated", "access_token": ref.access_token}



        # print('User id:',user_id)
        # user = StudentModel.find_by_id(user_id)
        # print('User:',user)
        # auth_header = user.to_json_access_token()
        # print('Auther Header:',auth_header)
        # user.save()
        # return 'signout'