#!/usr/bin/python3
"""
Module for unittests for the Review class
"""
import unittest
import os
import models
from models.review import Review


class TestReviewCreation(unittest.TestCase):
    """Test class for instantiating Review instance"""

    def setUp(self):
        self.file = 'file.json'
        try:
            os.remove(self.file)
        except:
            pass
        self.x = Review()
        self.validAttributes = {
            'place_id': str,
            'user_id': str,
            'text': str
            }
        self.storage = models.storage

    def tearDown(self):
        try:
            os.remove(self.file)
        except:
            pass

    def createReview(self):
        self.ex = Review()
        self.ex.place_id = "23asdk"
        self.ex.user_id = "asdfoie"
        self.ex.text = "text"

    def test_has_correct_class_name(self):
        self.assertEqual('Review', self.x.__class__.__name__)

    def test_empty_has_attrs(self):
        for k in self.validAttributes:
            self.assertTrue(hasattr(self.x, k))

    def test_empty_attrs_type(self):
        for k, v in self.validAttributes.items():
            test_type = type(getattr(self.x, k))
            self.assertEqual(test_type, v)

    def test_added_attrs(self):
        self.createReview()
        self.assertEqual(self.ex.place_id, "23asdk")
        self.assertEqual(self.ex.user_id, "asdfoie")

    def test_check_custom_attrs(self):
        self.x.custom_attr = "Test"
        self.assertEqual(self.x.custom_attr, "Test")
        self.assertIsInstance(self.x.custom_attr, str)

    def test_save_time_change(self):
        old_time = self.x.updated_at
        self.x.save()
        self.assertNotEqual(self.x.updated_at, old_time)

    def test_new_dict(self):
        self.createReview()
        dict_ = self.ex.to_dict()
        self.y = Review(**dict_)
        self.assertEqual(self.ex.place_id, self.y.place_id)

    def test_new_dict_attr_types(self):
        self.createReview()
        dict_ = self.ex.to_dict()
        self.y = Review(**dict_)
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
