import os
import mysql.connector

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

# username = os.getenv("DB_USERNAME", "root")
# password = os.getenv("DB_PASSWORD","1234")
# host = os.getenv("DB_HOST", "localhost")
# database = os.getenv("DB_NAME", "washim")

# SQLALCHEMY_DATABASE_URI  = "mysql+pymysql://{}:{}@{}/{}".format(username, password,host, database)
# # SQLALCHEMY_TRACK_MODIFICATIONS = False
# print(SQLALCHEMY_DATABASE_URI )


# Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="washim"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

# View All Database
for x in mycursor:
    print(x)
def abc(sql, value):
    mycursor.execute(sql, value)
    mydb.commit()



