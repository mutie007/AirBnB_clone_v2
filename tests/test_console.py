#!/usr/bin/python3
"""Test module for the console"""
import unittest
import os
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand


class TestConsole(unittest.TestCase):
    """Tests for the HBNB console"""

    def test_help(self):
        """Test help command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            self.assertIn("Documented commands", f.getvalue())

    def test_quit(self):
        """Test quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF(self):
        """Test EOF command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_emptyline(self):
        """Test empty line"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
            self.assertEqual(f.getvalue(), "")

    def test_create_missing_class(self):
        """Test create with missing class"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual("** class name missing **\n", f.getvalue())

    def test_create_invalid_class(self):
        """Test create with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_show_missing_class(self):
        """Test show with missing class"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            self.assertEqual("** class name missing **\n", f.getvalue())

    def test_show_invalid_class(self):
        """Test show with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

    def test_destroy_missing_class(self):
        """Test destroy with missing class"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            self.assertEqual("** class name missing **\n", f.getvalue())

    def test_create_with_params(self):
        """Test create with parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State name="California"')
            state_id = f.getvalue().strip()
            self.assertTrue(len(state_id) > 0)

    def test_create_with_string_param(self):
        """Test create with string parameter containing underscore"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create Place name="My_little_house"')
            place_id = f.getvalue().strip()
            self.assertTrue(len(place_id) > 0)

    def test_create_with_number_params(self):
        """Test create with integer and float parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                'create Place number_rooms=4 price_by_night=300 latitude=37.77')
            place_id = f.getvalue().strip()
            self.assertTrue(len(place_id) > 0)


if __name__ == "__main__":
    unittest.main()
