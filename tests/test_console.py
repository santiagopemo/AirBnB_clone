#!/usr/bin/python3
"""
TestConsole Module
"""
import unittest
import pep8
import models
import inspect
import os
import console
from io import StringIO
from unittest.mock import patch
HBNBCommand = console.HBNBCommand
current_module = console
test_path = 'console.py'
current_path = 'tests/test_console.py'


class TestConsole(unittest.TestCase):
    """TestConsole class"""

    def test_pep8(self):
        """Check PEP8 style"""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(
                                       [
                                        test_path,
                                        current_path
                                       ]
                                      )
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_empty_line(self):
        """Test empty line function"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
            self.assertEqual("", f.getvalue())
            HBNBCommand().onecmd("   ")
            self.assertEqual("", f.getvalue())
            HBNBCommand().onecmd("\n")
            self.assertEqual("", f.getvalue())

    def test_quit(self):
        """Test quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertEqual(HBNBCommand().onecmd("quit"), True)

    def test_quit(self):
        """Test EOF command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertEqual(HBNBCommand().onecmd("EOF"), True)

    def test_help(self):
        """Test help command"""
        h_out = ("Documented commands (type help <topic>):\n"
                 "========================================\n"
                 "EOF  all  count  create  destroy  help  quit  show  update")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            self.assertEqual(h_out, f.getvalue().strip())

    def test_help_EOF(self):
        """Test help EOF command"""
        h_out = ("Exits the program")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
            self.assertEqual(h_out, f.getvalue().strip())

    def test_help_all(self):
        """Test help all command"""
        h_out = """
                Prints all string representation of all instances
                based or not on the class name
                """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help all")
            self.assertEqual(h_out.split(), f.getvalue().split())

    def test_help_count(self):
        """Test help count command"""
        h_out = """
                Retrieves the number of instances of a class
                """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help count")
            self.assertEqual(h_out.split(), f.getvalue().split())

    def test_help_create(self):
        """Test help create command"""
        h_out = """
                Creates a new instance of BaseModel, saves
                it (to the JSON file) and prints the id
                """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help create")
            self.assertEqual(h_out.split(), f.getvalue().split())

    def test_help_destroy(self):
        """Test help destroy command"""
        h_out = """
                Deletes an instance based on the class name and id
                """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
            self.assertEqual(h_out.split(), f.getvalue().split())

    def test_help_quit(self):
        """Test help quit command"""
        h_out = "Quit command to exit the program\n\n"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
            self.assertEqual(h_out, f.getvalue())

    def test_help_show(self):
        """Test help show command"""
        h_out = """
                Prints the string representation of an instance
                based on the class name and id
                """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help show")
            self.assertEqual(h_out.split(), f.getvalue().split())

    def test_help_update(self):
        """Test help update command"""
        h_out = """
                Updates an instance based on the class name
                and id by adding or updating attribute
                """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help update")
            self.assertEqual(h_out.split(), f.getvalue().split())


if __name__ == "__main__":
    unittest.main()
