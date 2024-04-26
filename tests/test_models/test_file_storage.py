#!/usr/bin/python3
"""Unit tests for FileStorage class"""

import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.state import State
from os import getenv


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db', "FileStorage not in use")
class TestFileStorageMethods(unittest.TestCase):
    """Test cases for FileStorage methods"""

    def setUp(self):
        """Set up test environment"""
        self.file_storage = FileStorage()
        self.file_storage.reload()

    def tearDown(self):
        """Tear down test environment"""
        self.file_storage._FileStorage__objects = {}
        self.file_storage.save()

    def test_get(self):
        """Test get method"""
        new_state = State(name="California")
        new_state.save()
        state_id = new_state.id

        retrieved_state = self.file_storage.get(State, state_id)

        self.assertEqual(retrieved_state, new_state)

    def test_count_all(self):
        """Test count method with no class argument"""
        count_before = len(self.file_storage.all())

        state1 = State(name="New York")
        state1.save()
        state2 = State(name="Texas")
        state2.save()

        count_after = len(self.file_storage.all())

        self.assertEqual(count_after, count_before + 2)

    def test_count_class(self):
        """Test count method with class argument"""

        state_count_before = len(self.file_storage.all(State))

        state1 = State(name="Florida")
        state1.save()
        state2 = State(name="Georgia")
        state2.save()

        state_count_after = len(self.file_storage.all(State))

        self.assertEqual(state_count_after, state_count_before + 2)


if __name__ == '__main__':
    unittest.main()
