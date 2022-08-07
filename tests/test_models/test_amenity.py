#!/usr/bin/python3
"""
Module for unittests for the Amenity class
"""
import unittest
import os
import models
from models.amenity import Amenity


class TestAmenityEmptyCreation(unittest.TestCase):
    """Test class for instantiating amenity"""

    def setUp(self):
        self.file = 'file.json'
        try:
            os.remove(self.file)
        except:
            pass
        self.x = Amenity()
        self.validAttributes = {
            'name': str,
            }
        self.storage = models.storage

    def tearDown(self):
        try:
            os.remove(self.file)
        except:
            pass

    def test_user_has_correct_class_name(self):
        self.assertEqual('Amenity', self.x.__class__.__name__)

    def test_empty_amenity_has_attrs(self):
        for k in self.validAttributes:
            self.assertTrue(hasattr(self.x, k))

    def test_empyt_amenity_attrs_type(self):
        for k, v in self.validAttributes.items():
            test_type = type(getattr(self.x, k))
            self.assertEqual(test_type, v)

    def test_amenity_added_attrs(self):
        self.x.name = "pool"
        self.assertEqual(self.x.name, "pool")

    def test_check_custom_attrs(self):
        self.x.custom_attr = "Test"
        self.assertEqual(self.x.custom_attr, "Test")
        self.assertIsInstance(self.x.custom_attr, str)

    # TODO: This fails occasionally
    def test_save_time_change(self):
        old_time = self.x.updated_at
        self.x.save()
        self.assertNotEqual(self.x.updated_at, old_time)

    def test_new_amenity_dict(self):
        self.x.name = "pool"
        dict_ = self.x.to_dict()
        self.y = Amenity(**dict_)
        self.assertEqual(self.x.name, self.y.name)

    def test_new_amenity_dict_attr_types(self):
        self.x.name = "pool"
        dict_ = self.x.to_dict()
        self.y = Amenity(**dict_)
        for k, v in self.validAttributes.items():
            test_type = type(getattr(self.y, k))
            self.assertEqual(test_type, v)

    def test_save_user(self):
        self.assertIsInstance(self.storage._FileStorage__objects, dict)
        self.storage.save()
        self.assertTrue(os.path.exists(self.file))
        self.assertTrue(os.stat(self.file).st_size != 0)

    def test_reload_amenity(self):
        x_id = self.x.id
        x_id_key = "{}.{}".format(self.x.__class__.__name__, self.x.id)
        self.storage.save()
        self.storage._FileStorage__objects = {}
        self.storage.reload()
        self.assertEqual(x_id,
                         self.storage._FileStorage__objects[x_id_key].id)
