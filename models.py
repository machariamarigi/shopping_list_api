from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base model contains common utilities"""

    __abstract__ = True
    uuid = db.Column(db.Integer, primary_key=True)

    def save(self):
        """Common method of saving to a database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Common method to delete from a database"""
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Common method to map a model in dictionary format."""
        dictionary_mapping = {
            attribute.name: getattr(self, attribute.name)
            for attribute in self.__table__.columns
        }
        return dictionary_mapping


class User(BaseModel):
    """Model the user"""
    __tablename__ = 'users'
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @property
    def password(self):
        """Return password harsh when someone tries to acces the password"""
        return self.password_hash

    @password.setter
    def password(self, password):
        """Generate a password hass"""
        self.password_hash = generate_password_hash(password)

    def authenticate_password(self, password):
        """Check password hashing"""
        return check_password_hash(self.password_hash, password)


class Shoppinglist(BaseModel):
    pass
