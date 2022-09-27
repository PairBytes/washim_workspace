import imp
from importlib.resources import path
from msilib import PID_TITLE
import profile
import uuid
import os
import boto3
from student import app
from werkzeug.utils import secure_filename

class UploadFile:


    @staticmethod
    def allowed_file(filename):
        
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']




    @staticmethod
    def upload_file(file, user_type=None, user_id=None,
                    file_name=None, content_type=None):
        # try:
            filename = file_name if file_name else file.filename
            print('FileName:',filename)
            content_type = content_type if content_type else file.content_type
            print('Content Type:',content_type)

            if not file:
                print('file:',file)
                return {"status":0, "err":"File cannot be blank", "message":""}
            if not UploadFile.allowed_file(filename):
                print('Upload file allowend extension:',UploadFile.allowed_file(filename))
                return {"status": 0, "err": f"File type {content_type} not allowed", "message": ""}
            else:
                print('Profile:',profile)
                file_path = f"{user_type}/{uuid.uuid4()}-{user_id}-{filename}"
                print('File Path:',file_path)

            
           
            # else:
            #     return {'status':0, 'err': 'Invalid Upload Type'}

           
            return {"status": 1, "message": "File has been uploaded successfully.",
                    "url":f"{app.config['STATIC_FILE_URL']}{file_path}"}
        # except Exception as e:
        #     app.logger.error("Handler:UploadFile:error: {}".format(str(e)))
        #     return {"status": 0, "message":"", "err": "There is a problem with saving the file. Please try again."}
