from django.test import TestCase
from .models import NotePad

class NotePadTests(TestCase):

#NotePad tests
    def test_npresult(self):
        tt = NotePad(comment = 'Das ist ein test.')
        self.assertEqual(str(tt), tt.comment)
        
    def test_np(self):
        self.assertEqual(str(NotePad._meta.db_table), 'notepad')
    