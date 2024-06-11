import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get('DEV_SECRET_KEY')
    DEBUG = True
    TESTING = False
    ENV = 'development'


class TestingConfig(Config):
    SECRET_KEY = os.environ.get('TEST_SECRET_KEY')
    DEBUG = True
    TESTING = True
    ENV = 'testing'


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('PROD_SECRET_KEY')
    DEBUG = False
    TESTING = False
    ENV = 'production'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
