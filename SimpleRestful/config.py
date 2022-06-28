import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
LOG_FILE = 'hello.log'
LOG_LEVEL = 'DEBUG'

SECRET_KEY = 'thisissecretkey'


username = os.getenv("DB_USERNAME", "root")
password = os.getenv("DB_PASSWORD", "root1234")
server = os.getenv("DB_HOST", "localhost")
database = os.getenv("DB_NAME", "washim")

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(username, password, server, database)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
