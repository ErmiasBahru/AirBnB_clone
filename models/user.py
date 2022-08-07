#!/usr/bin/python3
"""
Module that holds the User Class
"""
from models.base_model import BaseModel


class User(BaseModel):
    """Class that represents a user"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
