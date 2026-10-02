#!/usr/bin/python3
"""Test module for DBStorage"""
import unittest
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "not testing database storage")
class TestDBStorage(unittest.TestCase):
    """Tests for the DBStorage class"""

    def test_db_storage_documentation(self):
        """Test that the module is documented"""
        self.assertIsNotNone(__import__('models.engine.db_storage').__doc__)


if __name__ == "__main__":
    unittest.main()
