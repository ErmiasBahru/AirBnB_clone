#!/usr/bin/python3
"""
Module for unittests for the BaseModel class
"""
import unittest
import datetime
from models.base_model import BaseModel


class TestBaseModelClassCreation(unittest.TestCase):
    """Test class for Base class instantiation tests"""

    def setUp(self):
        self.x = BaseModel()

    def test_id_creation(self):
        self.assertIsNotNone(self.x.id)
        self.assertEqual(36, len(self.x.id))
        self.assertIsInstance(self.x.id, str)
        self.assertFalse(" " in self.x.id)

    def test_created_at(self):
        self.assertIsNotNone(self.x.created_at)
        self.assertIsInstance(self.x.created_at, datetime.datetime)

    def test_updated_at(self):
        self.assertIsNotNone(self.x.updated_at)
        self.assertIsInstance(self.x.updated_at, datetime.datetime)

    def test_created_at_diff_updated_at(self):
        self.assertNotEqual(self.x.updated_at, self.x.created_at)
        time_diff = self.x.updated_at - self.x.created_at
        self.assertTrue(time_diff.microseconds > 0)

    def test_save_method(self):
        old_time = self.x.updated_at
        self.x.save()
        self.assertNotEqual(old_time, self.x.updated_at)
        self.assertIsInstance(self.x.updated_at, datetime.datetime)

    def test_to_dict_method(self):
        dict_ = self.x.to_dict()
        self.assertIsInstance(dict_, dict)
        self.assertIsInstance(dict_['updated_at'], str)
        self.assertIsInstance(dict_['created_at'], str)
        self.assertEqual(dict_['__class__'],
                         self.x.__class__.__name__)


class TestBaseModelObjectCreation(unittest.TestCase):
    """
    Test class for Base Model instantiation with kwargs
    """

    def setUp(self):
        self.my_model = BaseModel()
        self.my_model.name = "Betty"
        self.my_model.my_number = 89
        self.my_model_json = self.my_model.to_dict()
        self.my_new_model = BaseModel(**self.my_model_json)

    def test_create_object_from_dict(self):
        self.assertIsInstance(self.my_new_model, BaseModel)
        self.assertEqual("Betty", self.my_new_model.name)
        self.assertEqual(89, self.my_new_model.my_number)
        self.assertIsNotNone(self.my_new_model.created_at)
        self.assertIsInstance(self.my_new_model.created_at,
                              datetime.datetime)
        self.assertIsInstance(self.my_new_model.updated_at,
                              datetime.datetime)
        self.assertFalse(self.my_model is self.my_new_model)

    def test_str_method(self):
        string = "[{}] ({}) {}".format(self.my_model.__class__.__name__,
                                       self.my_model.id,
                                       self.my_model.__dict__)
        self.assertEqual(string, str(self.my_model))
