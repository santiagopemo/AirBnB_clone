#!/usr/bin/python3
"""
TestFileStorage unittest Module
"""
import unittest
import pep8
import models
import inspect
import os
from time import sleep
import json
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.engine.file_storage import FileStorage
current_module = models.engine.file_storage
test_path = 'models/engine/file_storage.py'
current_path = 'tests/test_models/test_engine/test_file_storage.py'


class TestFileStorage(unittest.TestCase):
    """TestFileStorage class"""

    def setUp(self):
        """Executes before each test"""
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except IOError:
            pass

    def tearDown(self):
        """Executes after each test"""
        FileStorage._FileStorage__objects = {}
        try:
            os.remove("file.json")
        except IOError:
            pass

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

    def test_docstring(self):
        """Checks the docstring documentation"""
        self.assertTrue(len(current_module.__doc__) >= 1)
        self.assertTrue(len(FileStorage.__doc__) >= 1)
        methods = inspect.getmembers(
                                     FileStorage,
                                     inspect.isfunction
                                    )
        for m in methods:
            self.assertTrue(len(m[1].__doc__) >= 1)

    def test_file_storage_instance(self):
        """Test FileStorage instance"""
        fs = FileStorage()
        self.assertTrue(hasattr(fs, '_FileStorage__file_path'))
        self.assertTrue(hasattr(fs, '_FileStorage__objects'))
        self.assertIs(type(getattr(fs, '_FileStorage__file_path')), str)
        self.assertIs(type(getattr(fs, '_FileStorage__objects')), dict)
        fs_funcs = inspect.getmembers(fs)
        func_names = [fn[0] for fn in fs_funcs]
        self.assertIn('all', func_names)
        self.assertIn('new', func_names)
        self.assertIn('save', func_names)
        self.assertIn('reload', func_names)

    def test_instance_with_args(self):
        """Test Filestorage instance with args"""
        with self.assertRaises(TypeError):
            sf = FileStorage(1)
        with self.assertRaises(TypeError):
            sf = FileStorage(None)

    def test_all(self):
        """Test all fucntion"""
        fs = FileStorage()
        objs = fs.all()
        self.assertEqual(len(objs), 0)
        self.assertEqual(objs, {})
        bm = BaseModel()
        am = Amenity()
        us = User()
        st = State()
        ct = City()
        pl = Place()
        rv = Review()
        objs = fs.all()
        self.assertEqual(len(objs), 7)
        l_objs = [bm, am, us, st, ct, pl, rv]
        for o in l_objs:
            key = "{}.{}".format(o.__class__.__name__, o.id)
            self.assertIn(key, objs)
            self.assertIs(o, objs[key])

    def test_all_args(self):
        """Test all function with args"""
        fs = FileStorage()
        with self.assertRaises(TypeError):
            fs.all(1)
        with self.assertRaises(TypeError):
            fs.all(None)

    def test_new(self):
        """Test new function"""
        fs = FileStorage()
        bm = BaseModel()
        am = Amenity()
        us = User()
        st = State()
        ct = City()
        pl = Place()
        rv = Review()
        l_objs = [bm, am, us, st, ct, pl, rv]
        for o in l_objs:
            fs.new(o)
            key = "{}.{}".format(o.__class__.__name__, o.id)
            self.assertIn(key, fs.all())
            self.assertIs(o, fs.all()[key])

    def test_new_no_args(self):
        """Test new function with no arguments"""
        fs = FileStorage()
        with self.assertRaises(TypeError):
            fs.new()

    def test_new_two_args(self):
        """Test new function with two arguments"""
        fs = FileStorage()
        bm = BaseModel()
        pl = Place()
        with self.assertRaises(TypeError):
            fs.new(bm, 3)
        with self.assertRaises(TypeError):
            fs.new(bm, pl)

    def test_new_wrong_args(self):
        """Test new function with wrong arguments"""
        fs = FileStorage()
        with self.assertRaises(AttributeError):
            fs.new(3)
        with self.assertRaises(AttributeError):
            fs.new(None)
        with self.assertRaises(AttributeError):
            fs.new("BaseModel")

    def test_save(self):
        """Test save function"""
        fs = FileStorage()
        bm = BaseModel()
        am = Amenity()
        us = User()
        st = State()
        ct = City()
        pl = Place()
        rv = Review()
        fs.save()
        with open('file.json') as f:
            objs = json.load(f)
        l_objs = [bm, am, us, st, ct, pl, rv]
        for o in l_objs:
            fs.new(o)
            key = "{}.{}".format(o.__class__.__name__, o.id)
            self.assertIn(key, objs)

    def test_save_args(self):
        """Test save function with arguments"""
        fs = FileStorage()
        with self.assertRaises(TypeError):
            fs.save(None)
        with self.assertRaises(TypeError):
            fs.save(2)

    def test_reload(self):
        """Test reload function"""
        fs = FileStorage()
        bm = BaseModel()
        am = Amenity()
        us = User()
        st = State()
        ct = City()
        pl = Place()
        rv = Review()
        fs.save()
        FileStorage._FileStorage__objects = {}
        self.assertEqual(fs.all(), {})
        self.assertEqual(len(fs.all()), 0)
        fs.reload()
        self.assertNotEqual(fs.all(), {})
        objs = fs.all()
        l_objs = [bm, am, us, st, ct, pl, rv]
        for o in l_objs:
            key = "{}.{}".format(o.__class__.__name__, o.id)
            self.assertIn(key, objs)

    def test_reload_args(self):
        """Test reload function with arguments"""
        fs = FileStorage()
        with self.assertRaises(TypeError):
            fs.reload(None)
        with self.assertRaises(TypeError):
            fs.reload(2)


if __name__ == "__main__":
    unittest.main()
