#!/usr/bin/python3
"""UserType model for the project"""
from models.database import db
from flask_login import UserMixin


class UserType(db.Model, UserMixin):
    """UserType model for the project"""
    __tablename__ = 'user_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, default=2)

    def __init__(self, name, description, user_id=2):
        self.name = name
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return vars(UserType)

    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id
        }
