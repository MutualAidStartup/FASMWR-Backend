import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'i-need-to-change-this'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # we need this because we're developing on localhost
    AUTHLIB_INSECURE_TRANSPORT = True


class ProductionConfig(BaseConfig):
    DEBUG = False


class StagingConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True