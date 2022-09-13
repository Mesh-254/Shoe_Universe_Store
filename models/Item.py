#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.
# This file has been modified by Meshack.

""""Items model class for the project"""

from flask_login import UserMixin
from models.database import db


# from sqlalchemy import DECIMAL


class Item(db.Model, UserMixin):
    """Item model for the project"""
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    categoryId = db.Column(db.ForeignKey('categories.id', ondelete='CASCADE',
                                         onupdate='CASCADE'),
                           nullable=False, index=True)
    category = db.relationship('Category')

    def __int__(self, price, name, image):
        """initialize the price attributes"""
        self.price = price,
        self.name = name,
        self.image = image

    def __repr__(self):
        """return a string representation of attributes"""
        return vars(Item)

    def serialize(self):
        """serialize the item"""
        return {
            "id": self.id,
            "price": self.price,
            "name": self.name,
            "image": self.image
        }
