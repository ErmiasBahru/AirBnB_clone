#!/usr/bin/python3
"""
Module for unittests for the FileStorage class
"""
import unittest
import os
import datetime
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
import models


class TestFileStorageClassCreation(unittest.TestCase):
    """Test class for Storage class instantiation tests"""

    def setUp(self):
        self.file = 'file.json'
        try:
            os.remove(self.file)
        except:
            pass
        self.x = BaseModel()
        self.fs = FileStorage()
        self.storage = models.storage

    def tearDown(self):
        try:
            os.remove(self.file)
        except:
            pass

    def test_inheritance(self):
        self.assertIsInstance(self.fs, FileStorage)

    def test_fs_has_class_attributes(self):
        self.assertIsInstance(self.fs._FileStorage__file_path, str)
        self.assertIsInstance(self.fs._FileStorage__objects, dict)

    def test_inheritance_storage(self):
        self.assertIsInstance(self.storage, FileStorage)

    def test_fs_has_class_attributes_storage(self):
        self.assertIsInstance(self.storage._FileStorage__file_path, str)
        self.assertIsInstance(self.storage._FileStorage__objects, dict)

    def test_fs_attributes_private(self):
        fs = FileStorage()
        with self.assertRaises(Exception):
            fs.__objects
        with self.assertRaises(Exception):
            fs.__file_path
        with self.assertRaises(Exception):
            getattr(fs, '__objects')
        with self.assertRaises(Exception):
            getattr(fs, '__file_path')

    def test_creation_with_arg(self):
        with self.assertRaises(Exception):
            fs = FileStorage(3)
        with self.assertRaises(Exception):
            fs = FileStorage("hello")
        with self.assertRaises(Exception):
            fs = FileStorage([])

    def test_all_method(self):
        self.assertIsInstance(self.storage.all(), dict)
        count = len(self.storage.all())
        self.assertTrue(count != 0)

    def test_new_method(self):
        x = BaseModel()
        obj_key = "{}.{}".format(x.__class__.__name__, x.id)
        self.storage.new(x)
        self.assertTrue(obj_key in self.storage._FileStorage__objects)
        self.assertIsInstance(self.storage._FileStorage__objects[obj_key],
                              BaseModel)
        temp_bm = self.storage._FileStorage__objects[obj_key]
        self.assertEqual(temp_bm.__class__.__name__,
                         'BaseModel')
        self.assertEqual(temp_bm.id, x.id)

    def test_new_method_1(self):
        count = len(self.storage.all())
        y = BaseModel()
        new_count = len(self.storage.all())
        self.assertEqual(count + 1, new_count)
        self.assertEqual(y.__class__.__name__, 'BaseModel')
        self.assertTrue(hasattr(y, 'created_at'))
        self.assertTrue(hasattr(y, 'updated_at'))

    def test_save_method(self):
        # self.assertIsInstance(self.storage._FileStorage__objects, dict)
        self.x = BaseModel()
        self.storage.save()
        self.assertTrue(os.path.exists(self.file))
        self.assertTrue(os.stat(self.file).st_size != 0)

    def test_reload_method(self):
        self.x = BaseModel()
        self.x.custom = "Warriors"
        x_id_key = "{}.{}".format(self.x.__class__.__name__, self.x.id)
        self.storage.new(self.x)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        temp_obj = self.storage._FileStorage__objects[x_id_key]
        self.assertEqual(self.x.id,
                         temp_obj.id)
        self.assertEqual(self.x.created_at,
                         temp_obj.created_at)
        self.assertEqual(self.x.updated_at,
                         temp_obj.updated_at)
        self.assertEqual(self.x.custom,
                         temp_obj.custom)
        self.assertIsInstance(self.x.id,
                              str)
        self.assertIsInstance(self.x.created_at,
                              datetime.datetime)
        self.assertIsInstance(self.x.updated_at,
                              datetime.datetime)
        self.assertIsInstance(self.x.custom,
                              str)

    def test_str_method(self):
        string = "[{}] ({}) {}".format(self.x.__class__.__name__,
                                       self.x.id,
                                       self.x.__dict__)
        self.assertEqual(string, str(self.x))
