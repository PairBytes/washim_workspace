from student_app import api
from student_app.controller.student_cotroller import Student_Csv, Csv_file

api.add_resource(Student_Csv, '/api/v1/csv')
api.add_resource(Csv_file, '/api/csvfile')