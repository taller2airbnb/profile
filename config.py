import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    GOOGLE_VALIDATOR = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'b\'\xc5>`\xe3C\x19\x13\xdc\xeaV\xefT\x9d\xa4x\xae\''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_SUPPRESS_SEND = False
    MAIL_DEBUG = True
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class ProductionConfig(Config):
    DEBUG = False
    START_DB = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentInDockerConfig(Config):
    ENV = "development"
    DEBUG = True
    START_DB = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@profile_db_1:5432/postgres'


class TestingWithoutDBConfig(Config):
    ENV = "development"
    TESTING = True
    DEBUG = True
    START_DB = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/postgres'


class TestingWithDBConfig(Config):
    ENV = "development"
    TESTING = True
    DEBUG = True
    START_DB = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/postgres'


class TestingWithValidGoogle(Config):
    ENV = "development"
    TESTING = True
    DEBUG = True
    START_DB = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/postgres'
    GOOGLE_VALIDATOR = "http://project_google_1:3000/valid_token"