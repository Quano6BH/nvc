class Config(object):
   SECRET_KEY = os.environ.get('SECRET_KEY')
   SQLALCHEMY_COMMIT_ON_TEARDOWN = True
   SQLALCHEMY_TRACK_MODIFICATIONS = False