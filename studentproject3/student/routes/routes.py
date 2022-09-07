from student import api
from student.controllers.student_controller import CustomSignup, ValidateEmailOTP, Student, CustomSigout, ForgotPassword, ResetPassword


api.add_resource(CustomSignup, '/api/v1/student/signup')
api.add_resource(ValidateEmailOTP, '/api/v1/validate_email/otp')
api.add_resource(Student, '/api/v1/student', '/api/v1/student/<user_id>')
api.add_resource(ForgotPassword, '/api/v1/forgot_password')
api.add_resource(CustomSigout, '/api/v1/student/signout')
api.add_resource(ResetPassword, '/api/v1/reset_password')