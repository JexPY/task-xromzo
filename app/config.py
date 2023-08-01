class Config(object):
    FLASK_ENV = "development"
    FLASK_DEBUG = False
    TESTING = False
    FLASK_APP = "app"


class ProductionConfig(Config):
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    FLASK_DEBUG = True


class TestingConfig(Config):
    FLASK_ENV = "testing"
    TESTING = True
    FLASK_DEBUG = True


default = "DevelopmentConfig"
