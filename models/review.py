#!/usr/bin/python3
"""
This module contains the Review Class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Class for the Review model"""

    place_id = ""
    user_id = ""
    text = ""
