import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

username = os.getenv("DB_USERNAME", "root")
password = os.getenv("DB_PASSWORD","1234")
host = os.getenv("DB_HOST", "localhost")
database = os.getenv("DB_NAME", "washim")

SQLALCHEMY_DATABASE_URI  = "mysql+pymysql://{}:{}@{}/{}".format(username, password,host, database)
# SQLALCHEMY_TRACK_MODIFICATIONS = False
print(SQLALCHEMY_DATABASE_URI )