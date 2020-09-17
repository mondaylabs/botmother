import os
from django.test import TestCase

from botmother.utils.api import clear_test_requests


class TelegramTestCase(TestCase):
    def tearDown(self):
        clear_test_requests()

    @classmethod
    def setUpClass(cls):
        clear_test_requests()
        super().setUpClass()

    def load(self, file):
        path = os.path.abspath(os.path.dirname(__file__))
        f = open(path + '/webhook/' + file, 'r')
        return f.read()
