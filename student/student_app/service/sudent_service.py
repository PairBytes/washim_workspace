from student_app.models.student_model import Student
from student_app import db
import os
import app
import pandas as pd
import config

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print('BASE_DIR:',BASE_DIR)
STATIC_DIR=os.path.join(BASE_DIR,'static')
print('TEMPLATE_DIR:',STATIC_DIR)


def parseCSV(filePath):
      # CVS Column Names
      col_names = ['Name','Mobile','Address', 'Education']
      print('column Name:',col_names)
      # Use Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      print('CSV Data:',csvData)
      # Loop through the Rows
      for i,row in csvData.iterrows():
            sql = "INSERT INTO Student_Table (Name, Mobile, Address, Education) VALUES (%s, %s, %s, %s)"
            print('SQL:',sql)
            value = (row['Name'],row['Mobile'],row['Address'],row['Education'])
            # print('SQL:',sql)
            print('values:',value)

            print(i,row['Name'],row['Mobile'],row['Address'],row['Education'])



class StudentService:
    def uploadFiles(self, file):
      print('uploaded file :',file)
      print('file.filename:',file.filename !='')
      # get the uploaded file
      if file.filename != '':
        file_path = os.path.join(STATIC_DIR, file.filename)
        print('file path:',file_path)
        # set the file path
        file.save(file_path)
        parseCSV(file_path)
          # save the file
      return "File Uploaded to read data and insert into table"
    
    