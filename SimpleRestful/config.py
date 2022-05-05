import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
LOG_FILE = 'hello.log'
LOG_LEVEL = 'DEBUG'

SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
