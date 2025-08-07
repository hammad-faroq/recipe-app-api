from django.test import SimpleTestCase
from app.calc import add1


class calcTests(SimpleTestCase):
    """The test calss for testing the fuction defined"""
    def test_add_numbers(self):
        res = add1(5,6)
        self.assertEqual(res, 11)
#when we use the test prefix, the method got automaticlly picked up by the test library we are using, unittest, djnago.test, djago_rest_framwork.text etc etc
