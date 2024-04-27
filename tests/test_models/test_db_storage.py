#!/usr/bin/python3
"""Unit tests for DBStorage class"""

import unittest
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.state import State
from os import getenv

@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', "DBStorage not in use")
class TestDBStorageMethods(unittest.TestCase):
    """Test cases for DBStorage methods"""

    def setUp(self):
        """Set up test environment"""
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        """Tear down test environment"""
        self.db.close()

    def test_get(self):
        """Test get method"""

        new_state = State(name="California")
        new_state.save()
        state_id = new_state.id

        retrieved_state = self.db.get(State, state_id)

        self.assertEqual(retrieved_state, new_state)

    def test_count_all(self):
        """Test count method with no class argument"""
        count_before = self.db.count()

        state1 = State(name="New York")
        state1.save()
        state2 = State(name="Texas")
        state2.save()

        count_after = self.db.count()

        self.assertEqual(count_after, count_before + 2)

    def test_count_class(self):
        """Test count method with class argument"""
        state_count_before = self.db.count(State)

        state1 = State(name="Florida")
        state1.save()
        state2 = State(name="Georgia")
        state2.save()

        state_count_after = self.db.count(State)

        self.assertEqual(state_count_after, state_count_before + 2)

if __name__ == '__main__':
    unittest.main()
