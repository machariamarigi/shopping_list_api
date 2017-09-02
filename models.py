from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel():
    """Base model contains common utilities"""
    def save(self):
        pass

    def delete(self):
        pass

    def serealize(self):
        pass
