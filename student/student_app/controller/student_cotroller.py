
from flask_restful import Resource, reqparse
from student_app import app
from student_app.models.student_model import Student
import werkzeug
from student_app.service.sudent_service import StudentService


class Student_Csv(Resource):
    def get(self):
        return "Hello! Welcome to APIs which will add students via CSV"

class Csv_file(Resource):
    def post(self):
        # try:
            parse = reqparse.RequestParser()
            print('Parse:',reqparse)
            parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
            args = parse.parse_args()
            print('Args:',args)
            csv_file = args['file']
            print('CSV file:', csv_file)
            # return 'file selected'
            return StudentService().uploadFiles(args['file'])
        # except:
        #     return 'select file'
