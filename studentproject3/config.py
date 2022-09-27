import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
LOG_FILE = 'student.log'
LOG_LEVEL = 'DEBUG'

SECRET_KEY = 'thisissecretkey'


username = os.getenv("DB_USERNAME", "root")
password = os.getenv("DB_PASSWORD", "1234")
server = os.getenv("DB_HOST", "localhost")
database = os.getenv("DB_NAME", "studentproject3")

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(username, password, server, database)
# SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False


PROFILE_PIC_PATH = 'static/profile/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
IMAGE_BASE_URL = ''

S3_REGION_NAME = os.getenv("S3_REGION_NAME", "")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "")
S3_ACL = 'public-read'
S3_DIR = 'student/'
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "")
S3_CACHE_CONTROL = os.getenv("S3_CACHE_CONTROL", "")

# ALLOWED_EXTENSIONS = {
#                         'profile': ['jpg', 'jpeg', 'png', 'gif']
#                      }
