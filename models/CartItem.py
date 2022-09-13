#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.
# This file has been modified by Meshack
#
"""cart model for the project"""


from models.database import db
from flask_login import UserMixin


class CartItem(db.Model, UserMixin):
    """cart items model for the project"""
    __tablename__ = "cart_items"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.ForeignKey("items.id",
                                      ondelete='CASCADE', onupdate='CASCADE'))
    user_id = db.Column(db.ForeignKey('users.id',
                                      ondelete='CASCADE', onupdate='CASCADE'),
                        nullable=False, index=True)
    item = db.relationship('Item')
    users = db.relationship('User')
