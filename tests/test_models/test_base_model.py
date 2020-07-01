#!/usr/bin/python3
"""
BaseModel unittest Module
"""
import unittest
import pep8
import models
import inspect
import os
from time import sleep
import json
from datetime import datetime
CurrentTestClass = models.base_model.BaseModel
current_module = models.base_model
file_name = os.path.basename(__file__)
current_path = "tests/test_models/{}".format(file_name)
test_path = "models/{}".format(file_name[5:])
cls_attr = ['id', 'created_at', 'updated_at']


class TestBaseModel(unittest.TestCase):
    """TestBaseModel class"""

    def setUp(self):
        """Executes before each test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def tearDown(self):
        """Executes when test finish"""
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
        self.assertTrue(len(CurrentTestClass.__doc__) >= 1)
        methods = inspect.getmembers(
                                     CurrentTestClass,
                                     inspect.isfunction
                                    )
        for m in methods:
            self.assertTrue(len(m[1].__doc__) >= 1)

    def test_base_model_single_instance(self):
        """Test a single instance"""
        cti1 = CurrentTestClass()
        for attr in cls_attr:
            self.assertTrue(hasattr(cti1, attr))
        self.assertEqual(type(cti1.id), str)
        self.assertEqual(type(cti1.created_at), datetime)
        self.assertEqual(type(cti1.updated_at), datetime)
        bm_funcs = inspect.getmembers(cti1)
        func_names = [fn[0] for fn in bm_funcs]
        self.assertIn('save', func_names)
        self.assertIn('to_dict', func_names)

    def test_two_instances(self):
        """Test two instances"""
        cti1 = CurrentTestClass()
        cti2 = CurrentTestClass()
        self.assertNotEqual(cti1.id, cti2.id)
        self.assertNotEqual(cti1.created_at, cti2.created_at)
        self.assertLess(cti1.created_at, cti2.created_at)
        self.assertNotEqual(cti1.updated_at, cti2.updated_at)
        self.assertLess(cti1.updated_at, cti2.updated_at)
        self.assertIsNot(cti1, cti2)

    def test_str_method(self):
        """Test str method"""
        cti1 = CurrentTestClass()
        cti1.id = "1234"
        cti1.name = "Holberton"
        cti1.my_number = 89
        cti1_dict = {
                    'id': cti1.id,
                    'created_at': repr(cti1.created_at),
                    'updated_at': repr(cti1.updated_at),
                    'name': 'Holberton',
                    'my_number': 89,
                   }
        cls_id = "[{}] (1234)".format(CurrentTestClass.__name__)
        self.assertIn(cls_id, cti1.__str__())
        for k, v in cti1_dict.items():
            self.assertIn(str(k), cti1.__str__())
            self.assertIn(str(v), cti1.__str__())

    def test_with_kwarg(self):
        """Test instance with **kwarg"""
        date = datetime.now().isoformat()
        cti1 = CurrentTestClass(id='12345', created_at=date, updated_at=date)
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(cti1.id, "12345")
        self.assertEqual(str(cti1.created_at), str(date))
        self.assertEqual(str(cti1.updated_at), str(date))

    def test_with_more_kwarg(self):
        """Test instance with extra **kwarg"""
        date = datetime.now().isoformat()
        cti1 = CurrentTestClass(id='12345', created_at=date, updated_at=date,
                                name='Santiago', age=28)
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(cti1.id, "12345")
        self.assertEqual(str(cti1.created_at), str(date))
        self.assertEqual(str(cti1.updated_at), str(date))
        self.assertEqual(cti1.name, "Santiago")
        self.assertIs(type(cti1.name), str)
        self.assertEqual(cti1.age, 28)
        self.assertIs(type(cti1.age), int)

    def test_with_kwarg_class(self):
        """Test instance __class__ attr **kwarg"""
        date = datetime.now().isoformat()
        cti1 = CurrentTestClass(id='12345', created_at=date, updated_at=date,
                                __class__="AnotherClass")
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(cti1.id, "12345")
        self.assertEqual(str(cti1.created_at), str(date))
        self.assertEqual(str(cti1.updated_at), str(date))
        self.assertNotEqual(cti1.__class__, "AnotherClass")
        self.assertNotEqual(cti1.__class__, CurrentTestClass.__name__)

    def test_with_arg(self):
        """Test with instance args"""
        date = datetime.now().isoformat()
        cti1 = CurrentTestClass('12345', date, date)
        self.assertNotEqual(cti1.id, '12345')
        self.assertNotEqual(cti1.created_at, date)
        self.assertNotEqual(cti1.updated_at, date)

    def test_kwargs_None(self):
        """Test **kwargs with None"""
        with self.assertRaises(TypeError):
            CurrentTestClass(id=None, created_at=None, updated_at=None)
        cti1 = CurrentTestClass(None)
        self.assertNotIn(None, cti1.__dict__)

    def test_save(self):
        """Test save() function"""
        cti1 = CurrentTestClass()
        old_date = cti1.updated_at
        sleep(1)
        cti1.save()
        self.assertNotEqual(old_date, cti1.updated_at)
        old_date2 = cti1.updated_at
        sleep(1)
        cti1.save()
        self.assertNotEqual(old_date2, cti1.updated_at)

    def test_save_args(self):
        """Test save function with args"""
        cti = CurrentTestClass()
        with self.assertRaises(TypeError):
            cti.save(1)
        with self.assertRaises(TypeError):
            cti.save(None)

    def test_is_saving(self):
        """Test if it is saving in file.json"""
        cti1 = CurrentTestClass()
        sleep(1)
        cti1.save()
        with open('file.json') as f:
            cti1_list = json.load(f)
        key = "{}.{}".format(CurrentTestClass.__name__, cti1.id)
        self.assertIn(key, cti1_list)
        self.assertDictEqual(cti1.to_dict(), cti1_list[key])

    def test_to_dict(self):
        """Test to_dict function"""
        cti1 = CurrentTestClass()
        cti1_dict = cti1.to_dict()
        self.assertEqual(type(cti1_dict), dict)
        self.assertIn('updated_at', cti1_dict)
        self.assertIn('created_at', cti1_dict)
        self.assertIn('__class__', cti1_dict)
        self.assertNotEqual(cti1_dict, cti1.__dict__)

    def test_to_dict_args(self):
        """Test to_dict function with arguments"""
        cti = CurrentTestClass()
        with self.assertRaises(TypeError):
            cti.to_dict(1)
        with self.assertRaises(TypeError):
            cti.to_dict(None)

    def test_to_dict_new_attributes(self):
        """Test to_dict fucntion when new attributes are set"""
        cti1 = CurrentTestClass()
        cti1.name = 'Alejandro'
        cti1.age = 21
        cti1_dict = cti1.to_dict()
        self.assertIn('name', cti1_dict)
        self.assertIn('age', cti1_dict)
        self.assertEqual('Alejandro', cti1_dict['name'])
        self.assertEqual(21, cti1_dict['age'])

    def test_to_dict_datetime(self):
        """Test to_dict function with datetime attributes"""
        cti1 = CurrentTestClass()
        old_created = cti1.created_at
        old_updated = cti1.updated_at
        cti1_dict = cti1.to_dict()
        self.assertEqual(type(cti1_dict['created_at']), str)
        self.assertEqual(type(cti1_dict['updated_at']), str)
        self.assertNotEqual(cti1_dict['created_at'], old_created)
        self.assertNotEqual(cti1_dict['updated_at'], old_updated)


if __name__ == "__main__":
    unittest.main()
