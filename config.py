# More configuration variables:
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# https://flask.palletsprojects.com/en/1.1.x/config/

class Config(object):
    """
    Common configurations
    """
    # Put any configurations here that are common across all environments
    SECRET_KEY = 'zxckfowksf123'
    # SQLALCHEMY_DATABASE_URI = '<use_database>://<username>:<password>@<IP>/<database_name>'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flask_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """
    Testing configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flask_test_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}