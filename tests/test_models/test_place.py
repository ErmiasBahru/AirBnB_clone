#!/usr/bin/python3
"""
Module for unittests for the Place class
"""
import unittest
import os
import models
from models.place import Place


class TestPlaceCreation(unittest.TestCase):
    """Test class for instantiating place"""

    def setUp(self):
        self.file = 'file.json'
        try:
            os.remove(self.file)
        except:
            pass
        self.x = Place()
        self.validAttributes = {
            'city_id': str,
            'user_id': str,
            'name': str,
            'description': str,
            'number_rooms': int,
            'max_guest': int,
            'price_by_night': int,
            'latitude': float,
            'longitude': float,
            'amenity_ids': list,
            }
        self.storage = models.storage

    def tearDown(self):
        try:
            os.remove(self.file)
        except:
            pass

    def createPlace(self):
        self.ex = Place()
        self.ex.city_id = "23asdk"
        self.ex.user_id = "asdfoie"
        self.ex.name = "John"
        self.ex.description = "Nice"
        self.ex.number_rooms = 32
        self.ex.number_bathrooms = 3
        self.ex.max_guest = 4
        self.ex.price_by_night = 199
        self.ex.latitude = 13.2323
        self.ex.longitude = 165.2323
        self.ex.amenity_ids = ['amenity1',
                               'amenity2',
                               'amenity3']

    def test_has_correct_class_name(self):
        self.assertEqual('Place', self.x.__class__.__name__)

    def test_empty_has_attrs(self):
        for k in self.validAttributes:
            self.assertTrue(hasattr(self.x, k))

    def test_empty_attrs_type(self):
        for k, v in self.validAttributes.items():
            test_type = type(getattr(self.x, k))
            self.assertEqual(test_type, v)

    def test_added_attrs(self):
        self.createPlace()
        self.assertEqual(self.ex.city_id, "23asdk")
        self.assertEqual(self.ex.user_id, "asdfoie")
        self.assertEqual(self.ex.name, "John")
        self.assertEqual(self.ex.description, "Nice")
        self.assertEqual(self.ex.number_rooms, 32)
        self.assertEqual(self.ex.number_bathrooms, 3)
        self.assertEqual(self.ex.max_guest, 4)

    def test_check_custom_attrs(self):
        self.x.custom_attr = "Nga"
        self.assertEqual(self.x.custom_attr, "Nga")
        self.assertIsInstance(self.x.custom_attr, str)

    # #TODO: This fails occasionally
    def test_save_time_change(self):
        old_time = self.x.updated_at
        self.x.save()
        self.assertNotEqual(self.x.updated_at, old_time)

    def test_new_dict(self):
        self.createPlace()
        dict_ = self.ex.to_dict()
        self.y = Place(**dict_)
        self.assertEqual(self.ex.name, self.y.name)

    def test_new_dict_attr_types(self):
        self.createPlace()
        dict_ = self.ex.to_dict()
        self.y = Place(**dict_)
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
