"""Module for the application configuration"""


class Config(object):
    """Common configurations"""


class DevelopmentConfig(Config):
    """Development configurations"""
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configurations"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configurations"""
    TESTING = True
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
