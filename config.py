import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
    #     ['true', 'on', '1']
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # FLASKY_POSTS_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_HOST = os.environ.get('DEV_DATABASE_URL')
    MONGODB_DB = os.environ.get('DEV_DB_NAME')


class TestingConfig(Config):
    TESTING = True
    MONGODB_HOST = os.environ.get('TEST_DATABASE_URL') or  \
        "mongodb+srv://tsilahamer:Test1234@test-aq19y.mongodb.net/dev_test?retryWrites=true&w=majority"
    MONGODB_DB = os.environ.get('TEST_DB_NAME') or "dev_test"
    ENABLE_HUMAN_LOG_FILE = True
    HUMAN_LOG_FILE_PATH = "C:/Users/Tsila/Desktop/scripts/logs"

class ProductionConfig(Config):
    MONGODB_HOST = os.environ.get('DATABASE_URL') or  \
        "mongodb+srv://tsilahamer:Test1234@test-aq19y.mongodb.net/test?retryWrites=true&w=majority"
    MONGODB_DB = os.environ.get('DB_NAME') or "test"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

