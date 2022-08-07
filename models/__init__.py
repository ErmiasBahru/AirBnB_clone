#!/usr/bin/python3
"""Initialization for Models"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
