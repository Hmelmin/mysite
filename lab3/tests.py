
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from django.test import TestCase



from lab3.models import planes,airlines
import unittest

class Tests(unittest.TestCase):

    def test_plane(self):
         new_plane = planes(12,'An 225', 'cargo')
         new_plane.save()

    def test_airline(self):
        new_airline = airlines(7,'Fly Etihad')
        new_airline.save()


if __name__ == '__main__':

    unittest.main()
# Create your tests here.
