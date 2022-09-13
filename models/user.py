#!/usr/bin/python3
"""user model for the project"""
from models.database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """user model for the project"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.VARCHAR(300), unique=True, nullable=False)
    reset_password = db.Column(db.Integer, default=0)
    usertype_id = db.Column(db.ForeignKey('user_types.id',
                                          ondelete='CASCADE',
                                          onupdate='CASCADE'),
                            index=True)
    usertype = db.relationship('UserType')

    def __init__(self, username, email, password, usertype_id=2):
        """Initialize the user model"""
        self.username = username
        self.password = password
        self.email = email
        self.usertype_id = usertype_id

    def __repr__(self):
        return vars(User)

    def serialize(self):
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'usertype_id': self.usertype_id
        }
