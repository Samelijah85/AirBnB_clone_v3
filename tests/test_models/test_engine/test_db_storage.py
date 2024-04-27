#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
from os import getenv
import pycodestyle as pep8
import unittest

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', "DBStorage not in use")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    def setUp(self):
        """Set up test environment"""
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        """Tear down test environment"""
        self.db.close()

    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    def test_new(self):
        """test that new adds an object to the database"""
        state_data = {"name": "Blantyre"}
        new_state = State(**state_data)
        self.db.new(new_state)
        session = self.db.__session
        retrieved_state = session.query(State).filter_by(id=new_state).first()

        self.assertEqual(retrieved_state.id, new_state.id)
        self.assertEqual(retrieved_state.name, new_state.name)
        self.assertIsNone(retrieved_state)

    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state_data = {"name": "Lilongwe"}
        new_state = State(**state_data)
        self.db.new(new_state)
        self.db.save()
        session = self.db.__session

        retrieved_state = session.query(State).filter_by(id=new_state).first()

        self.assertEqual(retrieved_state.id, new_state.id)
        self.assertEqual(retrieved_state.name, new_state.name)
        self.assertIsNone(retrieved_state)

    def test_get(self):
        """Test get method"""
        storage = self.db
        storage.reload()
        state_data = {"name": "Zomba"}
        new_state = State(**state_data)
        new_state.save()

        retrieved_state = storage.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state)

        fake_state = storage.get(State, "fake_id")
        self.assertEqual(fake_state, None)

    def test_count(self):
        """Test count method"""
        storage = self.db
        count_before = storage.count()
        state_count_before = storage.count(State)

        new_state1 = State(name="Mzuzu")
        new_state1.save()
        new_state2 = State(name="Machinga")
        new_state2.save()

        count_after = storage.count()
        state_count_after = storage.count(State)
        self.assertEqual(count_after, count_before + 2)
        self.assertEqual(state_count_after, state_count_before + 2)
