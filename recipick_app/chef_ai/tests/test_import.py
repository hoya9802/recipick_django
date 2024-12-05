from django.test import SimpleTestCase


class TransformersTest(SimpleTestCase):
    def test_transformers_import(self):
        try:
            import transformers
            import torch

            _, _ = transformers, torch

            self.assertTrue(True)
        except ImportError:
            self.fail('import error')
