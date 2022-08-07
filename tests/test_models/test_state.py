#!/usr/bin/python3
"""
Module for unittests for the State class
"""
import unittest
import os
import models
from models.state import State


class TestStateCreation(unittest.TestCase):
    """Test class for instantiating state"""

    def setUp(self):
        self.file = 'file.json'
        try:
            os.remove(self.file)
        except:
            pass
        self.x = State()
        self.validAttributes = {
            'name': str,
            }
        self.storage = models.storage

    def tearDown(self):
        try:
            os.remove(self.file)
        except:
            pass

    def createState(self):
        self.ex = State()
        self.ex.name = "New York"

    def test_has_correct_class_name(self):
        self.assertEqual('State', self.x.__class__.__name__)

    def test_empty_has_attrs(self):
        for k in self.validAttributes:
            self.assertTrue(hasattr(self.x, k))

    def test_empty_attrs_type(self):
        for k, v in self.validAttributes.items():
            test_type = type(getattr(self.x, k))
            self.assertEqual(test_type, v)

    def test_added_attrs(self):
        self.createState()
        self.assertEqual(self.ex.name, "New York")

    def test_check_custom_attrs(self):
        self.x.custom_attr = "Test"
        self.assertEqual(self.x.custom_attr, "Test")
        self.assertIsInstance(self.x.custom_attr, str)

    def test_save_time_change(self):
        old_time = self.x.updated_at
        self.x.save()
        self.assertNotEqual(self.x.updated_at, old_time)

    def test_new_dict(self):
        self.createState()
        dict_ = self.ex.to_dict()
        self.y = State(**dict_)
        self.assertEqual(self.ex.name, self.y.name)

    def test_new_dict_attr_types(self):
        self.createState()
        dict_ = self.ex.to_dict()
        self.y = State(**dict_)
        for k, v in self.validAttributes.items():
            test_type = type(getattr(self.y, k))
            self.assertEqual(test_type, v)

    def test_save(self):
        self.assertIsInstance(self.storage._FileStorage__objects, dict)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file))
        self.assertTrue(os.stat(self.file).st_size != 0)

    def test_reload(self):
        x_id = self.x.id
        x_id_key = "{}.{}".format(self.x.__class__.__name__, self.x.id)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        self.assertEqual(x_id,
                         self.storage._FileStorage__objects[x_id_key].id)
