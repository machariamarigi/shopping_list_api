"""Module for the application configuration"""

import os


class Config(object):
    """Common configurations"""
    SQLALCHEMY_DATABASE_URI = os.getenv('db_url')
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('secret')


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
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('test_db') or 'sqlite:///:memory'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
