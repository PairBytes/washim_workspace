from datetime import datetime, date, timedelta
import pytz
import random
import string
import uuid
from hello_app.models.user_model import UsersModel
from hello_app.models.user_varification_model import UsrVerificationModel
from hello_app.helper.rest_response import RestResponse
from hello_app import app
from flask_jwt_extended import create_access_token




class UserService:
    # def __init__(self):
    #     self.user_activity_coll = Base_Mongo(exmyb_mongo_db, app.config['USER_ACTIVITY_LOGS'])
    #     self.user_validate_coll = Base_Mongo(exmyb_mongo_db, app.config['USR_VALIDATE_COLL'])

    def custom_signup(self, email, password, user_type, first_name, last_name, country_code, mobile_number,
                      department_type):
        try:
            user = UsersModel.find_by_email(email)
            if not user:
                if country_code and mobile_number:
                    if UsersModel.find_by_mobile(country_code.strip(), mobile_number.strip()):
                        return RestResponse(err="Mobile Number already exists.").to_json(), 400
                elif country_code and not mobile_number:
                    return RestResponse(err="Mobile Number can not be blank.").to_json(), 400
                elif not country_code and mobile_number:
                    return RestResponse(err="Country Code can not be blank.").to_json(), 400

                if self.generate_otp_email(email, user_type):
                    password = UsersModel.generate_password_hash(password)
                    user_uuid = str(uuid.uuid4())
                    user = UsersModel(email=email, password=password, user_type=user_type, first_name=first_name,
                                      last_name=last_name, country_code=country_code, mobile_number=mobile_number,
                                      signup_type='email', userid=user_uuid, created_at=datetime.utcnow(),
                                      updated_at=datetime.utcnow(), department_type=department_type
                                      )
                    user.temp_save()
                    user.created_by = user.updated_by = user.id
                    user.save()
                    return RestResponse(
                        {'email': email, 'user_type': user_type}, message='OTP has been sent to your email address',
                        status=1).to_json(), 201
                else:
                    return RestResponse(err='Error while sending mail for verification').to_json(), 500
            else:
                return RestResponse(err="User already exists!").to_json(), 403
        except Exception as e:
            app.logger.error("UserService:custom_signup:: {}".format(str(e)))
            return RestResponse(err='Something went wrong').to_json(), 500

    def generate_otp_email(self, email, user_type=None):
        try:
            otp = ""
            for i in range(4):
                otp += str(random.randint(0, 9))

            usr_verify = UsrVerificationModel(usr_type=user_type, verification_id=email, otp=otp, is_expired=False,
                                              verification_type='email', otp_time=datetime.utcnow(), attempts=0)
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
            # usr_verify.is_send = is_send
            # usr_verify.message = msg
            # usr_verify.save()
            print('Html_Body : ',html_body)
            return True
        except Exception as e:
            app.logger.error("UserService:generate_otp_email:: {}".format(str(e)))
            return False
    
    def validate_otp_email(self, email, user_type, otp, user=None):
        try:
            usr_verify = UsrVerificationModel.query.order_by(UsrVerificationModel.otp_time.desc()).filter_by(
                verification_id=email, usr_type=user_type).first()
            if usr_verify:
                if usr_verify.is_expired:
                    app.logger.info("user verify data is expired ....{}.".format(str(usr_verify.is_expired)))
                    return RestResponse(err="OTP has been expired!").to_json(), 410
                elif otp.strip() == usr_verify.otp:
                    otp_time = int(
                        (datetime.utcnow() - usr_verify.otp_time).total_seconds() / 60)
                    app.logger.info("OTP Expire Now Time:{}".format(str(datetime.utcnow())))
                    app.logger.info("OTP Time:{}".format(str(usr_verify.otp_time)))
                    app.logger.info("OTP Time min:{}".format(str(otp_time)))
                    if otp_time > 15:
                        usr_verify.is_expired = True
                        usr_verify.save()
                        return RestResponse(err="OTP has been expired!").to_json(), 410
                    else:
                        if user:
                            user.email_verify = True
                            user.email = email
                        else:
                            user = UsersModel.find_by_email_and_usr_type(email, user_type)
                            user.email_verify = True
                            user.access_token = create_access_token(identity=str(user.userid), expires_delta=False)
                            # set client or vendor org profile
                            if user.user_type == 'client':
                                self.create_user_org_profile(user.id, user.user_type)
                        user.save()
                        if user.user_type in ['client', 'vendor']:
                            org_profiles = self.get_user_profiles(user.id, user.user_type)
                            user = user.to_json_access_token()
                            user['org_profiles'] = org_profiles
                        else:
                            user = user.to_json_access_token()
                        return RestResponse(user, message="Email Validated", status=1).to_json(), 201
                else:
                    return RestResponse(err='You entered invalid OTP.').to_json(), 400
            else:
                return RestResponse(err='Invalid Email Id.').to_json(), 400
        except Exception as e:
            app.logger.error("UserService:validate_otp_email:: {}".format(str(e)))
            return RestResponse(err=str(e)).to_json(), 500