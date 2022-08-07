#!/usr/bin/python3
"""
Module for unittests for the User class
"""
import unittest
import os
import json
import datetime
import models
from models.user import User
from models.base_model import BaseModel


class TestUserCreationEmpty(unittest.TestCase):
    """Test class for instantiating empty user"""

    def setUp(self):
        self.file = 'file.json'
        try:
            os.remove(self.file)
        except:
            pass
        self.x = User()
        self.validAttributes = {
            'email': str,
            'password': str,
            'first_name': str,
            'last_name': str
            }
        self.storage = models.storage

    def tearDown(self):
        try:
            os.remove(self.file)
        except:
            pass

    def test_user_has_correct_class_name(self):
        self.assertEqual('User', self.x.__class__.__name__)

    def test_empty_user_has_attrs(self):
        for k in self.validAttributes:
            self.assertTrue(hasattr(self.x, k))

    def test_empyt_user_attrs_type(self):
        for k, v in self.validAttributes.items():
            test_type = type(getattr(self.x, k))
            self.assertEqual(test_type, v)

    def test_user_added_attrs(self):
        self.x.first_name = "Betty"
        self.x.last_name = "Betty"
        self.x.email = "airbnb@mail.com"
        self.x.password = "root"
        self.assertEqual(self.x.first_name, "Betty")
        self.assertEqual(self.x.last_name, "Betty")
        self.assertEqual(self.x.email, "airbnb@mail.com")
        self.assertEqual(self.x.password, "root")

    def test_check_custom_attrs(self):
        self.x.custom_attr = "Test"
        self.assertEqual(self.x.custom_attr, "Test")
        self.assertIsInstance(self.x.custom_attr, str)

    # TODO: This fails occasionally
    def test_save_time_change(self):
        old_time = self.x.updated_at
        self.x.save()
        self.assertNotEqual(self.x.updated_at, old_time)

    def test_new_user_dict(self):
        self.x.first_name = "Betty"
        self.x.last_name = "Betty"
        self.x.email = "airbnb@mail.com"
        self.x.password = "root"
        dict_ = self.x.to_dict()
        self.y = User(**dict_)
        self.assertEqual(self.x.first_name, self.y.first_name)
        self.assertEqual(self.x.last_name, self.y.last_name)
        self.assertEqual(self.x.email, self.y.email)
        self.assertEqual(self.x.password, self.y.password)

    def test_new_user_dict_attr_types(self):
        self.x.first_name = "Betty"
        self.x.last_name = "Betty"
        self.x.email = "airbnb@mail.com"
        self.x.password = "root"
        dict_ = self.x.to_dict()
        self.y = User(**dict_)
        for k, v in self.validAttributes.items():
            test_type = type(getattr(self.y, k))
            self.assertEqual(test_type, v)

    def test_save_user(self):
        self.assertIsInstance(self.storage._FileStorage__objects, dict)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file))
        self.assertTrue(os.stat(self.file).st_size != 0)

    def test_reload_user(self):
        x_id = self.x.id
        x_id_key = "{}.{}".format(self.x.__class__.__name__, self.x.id)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        self.assertEqual(x_id,
                         self.storage._FileStorage__objects[x_id_key].id)


class TestUserCreation(unittest.TestCase):
    """Test class for User class instantiation tests"""

    def setUp(self):
        self.file = 'file.json'
        try:
            os.remove(self.file)
        except:
            pass
        self.x = User()
        self.x.first_name = "Betty"
        self.x.last_name = "Betty"
        self.x.email = "airbnb@mail.com"
        self.x.password = "root"
        self.x.save()
        self.fp = open('file.json', 'r', encoding="utf-8")
        self.dict_ = json.load(self.fp)
        self.validAttributes = {
            'email': str,
            'password': str,
            'first_name': str,
            'last_name': str
            }

    def tearDown(self):
        try:
            self.fp.close()
        except:
            pass
        try:
            os.remove(self.file)
        except:
            pass

    def test_test_all_attrs(self):
        for k, v in self.validAttributes.items():
            test_attr = getattr(self.x, k)
            self.assertIsInstance(test_attr, v)

    def test_user_creation(self):
        self.assertIsInstance(self.x, BaseModel)
        self.assertIsInstance(self.x, User)

    def test_is_classname(self):
        self.assertEqual(self.x.__class__.__name__, "User")

    def test_attr_type(self):
        self.assertIsInstance(self.x.email, str)
        self.assertIsInstance(self.x.password, str)
        self.assertIsInstance(self.x.first_name, str)
        self.assertIsInstance(self.x.last_name, str)
        self.assertIsInstance(self.x.updated_at, datetime.datetime)
        self.assertIsInstance(self.x.created_at, datetime.datetime)
        self.assertIsInstance(self.x.id, str)

    def test_has_attr(self):
        for k in self.validAttributes:
            self.assertTrue(hasattr(self.x, k))
        self.assertTrue(hasattr(self.x, 'updated_at'))
        self.assertTrue(hasattr(self.x, 'created_at'))
        self.assertTrue(hasattr(self.x, 'id'))

    def test_kwargs(self):
        a = User(password="psswd")
        self.assertEqual(a.password, "psswd")

    def test_attr_values(self):
        self.assertEqual(self.x.email,
                         "airbnb@mail.com")
        self.assertEqual(self.x.password, "root")
        self.assertEqual(self.x.first_name, "Betty")
        self.assertEqual(self.x.last_name, "Betty")

    def test_attr_is_saved(self):
        old_updated_at = self.x.updated_at
        self.x.save()
        self.assertNotEqual(old_updated_at, self.x.updated_at)

    def test_instance_is_in_storage(self):
        key = "{}.{}".format(self.x.__class__.__name__, self.x.id)
        self.assertTrue(key in self.dict_)

    def test_instance_storage_attrs(self):
        key = "{}.{}".format(self.x.__class__.__name__, self.x.id)
        self.x.save()

    def test_str_method(self):
        string = "[{}] ({}) {}".format(self.x.__class__.__name__,
                                       self.x.id,
                                       self.x.__dict__)
        self.assertEqual(string, str(self.x))

    def test_id_creation(self):
        self.x = User()
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
        self.x = User()
        dict_ = self.x.to_dict()
        self.assertIsInstance(dict_, dict)
        self.assertIsInstance(dict_['updated_at'], str)
        self.assertIsInstance(dict_['created_at'], str)
        self.assertEqual(dict_['__class__'],
                         self.x.__class__.__name__)
