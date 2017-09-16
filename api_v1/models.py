"""Module that contains the API's data models"""
from datetime import datetime, timedelta

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

import jwt

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base model contains common methods"""

    __abstract__ = True

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
    uuid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bucketlists = db.relationship(
        'Shoppinglist', backref='creator', lazy='dynamic')

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
        """Generate a password hash"""
        self.password_hash = generate_password_hash(password)

    def authenticate_password(self, password):
        """Check password hashing"""
        return check_password_hash(self.password_hash, password)

    def generate_token(self, user_id):
        """Generate the acces token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )

            return jwt_string
        except Exception as excep:
            return str(excep)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"

    def __repr__(self):
        """Return a representation of the user model instance"""
        return "<User: {}>".format(self.username)


class Shoppinglist(BaseModel):
    """Model for the shoppinglist"""
    __tablename__ = 'shoppinglists'

    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    items = db.relationship(
        'Shoppingitem', backref='creator', lazy='dynamic')

    def __repr__(self):
        """Return a representation of the shopping list model instance"""
        return "<Shopping List: {}>".format(self.name)


class Shoppingitem(BaseModel):
    """Class represents shoppingitems table"""
    __tablename__ = "shoppingitems"

    # Define columns for users table
    uuid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    quantity = db.Column(db.String(256))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())
    shoppinglist = db.Column(db.Integer, db.ForeignKey('shoppinglists.uuid'))

    def __repr__(self):
        """Return a representation of the Item model instance"""
        return "<Item: {}>".format(self.name)
