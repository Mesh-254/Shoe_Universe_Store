#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.
# This file has been modified by Meshack.

""""Items model class for the project"""


from flask_login import UserMixin
from models.database import db


class Category(db.Model, UserMixin):
    """Category model"""
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }
