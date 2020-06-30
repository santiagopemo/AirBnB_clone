#!/usr/bin/python3
"""
BaseModel unittest Module
"""
import unittest
import pep8
import models
import inspect
import os
from datetime import datetime
CurrentTestClass = models.base_model.BaseModel
current_module = models.base_model
file_name = os.path.basename(__file__)
current_path = "tests/test_models/{}".format(file_name)
test_path = "models/{}".format(file_name[5:])


class TestBaseModel(unittest.TestCase):
    """TestBaseModel class"""

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_pep8(self):
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
        self.assertTrue(len(current_module.__doc__) >= 1)
        self.assertTrue(len(CurrentTestClass.__doc__) >= 1)
        methods = inspect.getmembers(
                                     CurrentTestClass,
                                     inspect.isfunction
                                    )
        for m in methods:
            self.assertTrue(len(m[1].__doc__) >= 1)

    def test_base_model_single_instance(self):
        cti1 = CurrentTestClass()
        self.assertTrue(hasattr(cti1, 'id'))
        self.assertTrue(hasattr(cti1, 'created_at'))
        self.assertTrue(hasattr(cti1, 'updated_at'))
        self.assertEqual(type(cti1.id), str)
        self.assertEqual(type(cti1.created_at), datetime)
        self.assertEqual(type(cti1.updated_at), datetime)
        bm_funcs = inspect.getmembers(cti1)
        func_names = [fn[0] for fn in bm_funcs]
        self.assertIn('save', func_names)
        self.assertIn('to_dict', func_names)

    def test_two_instances(self):
        cti1 = CurrentTestClass()
        cti2 = CurrentTestClass()
        self.assertNotEqual(cti1.id, cti2.id)
        self.assertNotEqual(cti1.created_at, cti2.created_at)
        self.assertLess(cti1.created_at, cti2.created_at)
        self.assertNotEqual(cti1.updated_at, cti2.updated_at)
        self.assertLess(cti1.updated_at, cti2.updated_at)

    def test_str_method(self):
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
        cls_id = "[{}] (1234)".format(cti1.__class__.__name__)
        self.assertIn(cls_id, cti1.__str__())
        for k, v in cti1_dict.items():
            self.assertIn(str(k), cti1.__str__())
            self.assertIn(str(v), cti1.__str__())

    def test_with_kwarg(self):
        date = datetime.now().isoformat()
        cti1 = CurrentTestClass(id='12345', created_at=date, updated_at=date)
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
        self.assertEqual(cti1.id, "12345")
        self.assertEqual(str(cti1.created_at), str(date))
        self.assertEqual(str(cti1.updated_at), str(date))


if __name__ == "__main__":
    unittest.main()
