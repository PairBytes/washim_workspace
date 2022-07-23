from hello_app import api, app

from hello_app.Token.Token_Create import login
from hello_app.controllers.user_controller import CustomSignup, ValidateEmailOTP, Users, UserSearch


api.add_resource(CustomSignup, '/api/v1/user/signup')
api.add_resource(ValidateEmailOTP, '/api/v1/validate_email/otp')
api.add_resource(Users, '/api/v1/user', '/api/v1/user/<user_id>')
api.add_resource(UserSearch, '/api/v1/<user_type>/user_search')
