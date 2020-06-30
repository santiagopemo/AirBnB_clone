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
BaseModel = models.base_model.BaseModel


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
                                        'models/base_model.py',
                                        'tests/test_models/test_base_model.py'
                                       ]
                                      )
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_docstring(self):
        self.assertTrue(len(models.base_model.__doc__) >= 1)
        self.assertTrue(len(BaseModel.__doc__) >= 1)
        methods = inspect.getmembers(
                                     BaseModel,
                                     inspect.isfunction
                                    )
        for m in methods:
            self.assertTrue(len(m[1].__doc__) >= 1)

    def test_base_model_single_instance(self):
        bm1 = BaseModel()
        self.assertTrue(hasattr(bm1, 'id'))
        self.assertTrue(hasattr(bm1, 'created_at'))
        self.assertTrue(hasattr(bm1, 'updated_at'))
        self.assertEqual(type(bm1.id), str)
        self.assertEqual(type(bm1.created_at), datetime)
        self.assertEqual(type(bm1.updated_at), datetime)
        bm_funcs = inspect.getmembers(bm1)
        func_names = [fn[0] for fn in bm_funcs]
        self.assertIn('save', func_names)
        self.assertIn('to_dict', func_names)
        bm1_dict = {
                    '__class__': 'BaseModel',
                    'id': bm1.id,
                    'created_at': bm1.created_at.isoformat(),
                    'updated_at': bm1.updated_at.isoformat()
                   }
        self.assertDictEqual(bm1.to_dict(), bm1_dict)


if __name__ == "__main__":
    unittest.main()
