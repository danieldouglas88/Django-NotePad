from django.test import TestCase
from .models import NotePad
from django.urls import reverse
from datetime import datetime

#NotePad tests
class NotePadTests(TestCase):
    
    def test_comment(self):
        tt = NotePad(comment = 'Das ist ein test.')
        self.assertEqual(str(tt), tt.comment)
    
    def test_initdate(self):
        tt = NotePad(initialdate = None)
        self.assertEqual(str(tt), tt.comment)
        
    def test_upddate(self):
        tt = NotePad(update_date = None)
        self.assertEqual(str(tt), tt.comment)
        
    def test_username(self):
        tt = NotePad(username = None)
        self.assertEqual(str(tt), tt.comment)   
        
    def test_np(self):
        self.assertEqual(str(NotePad._meta.db_table), 'notepad')

#View tests
class IndexTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'), follow = True)
        self.assertEqual(response.status_code, 200)   
        
class CreateNotetest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('createnote'), follow = True)
        self.assertEqual(response.status_code, 200) 

class CreateSuccessTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('createsuccess'), follow = True)
        self.assertEqual(response.status_code, 200) 
        
class ErrorTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('error'), follow = True)
        self.assertEqual(response.status_code, 200) 
        
class NoteDeleteTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('notedelete'), follow = True)
        self.assertEqual(response.status_code, 200) 
        
class NoteDetailsTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('notedetails'), follow = True)
        self.assertEqual(response.status_code, 200)

class NoteUpdateTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('noteupdate'), follow = True)
        self.assertEqual(response.status_code, 200)     

class SearchTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('search'), follow = True)
        self.assertEqual(response.status_code, 200) 
        
class SearchResultTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('searchresult'), follow = True)
        self.assertEqual(response.status_code, 200) 
        
class SeeMyNotesTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('seemynotes'), follow = True)
        self.assertEqual(response.status_code, 200) 
        
class SeeNotesTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('seenotes'), follow = True)
        self.assertEqual(response.status_code, 200) 
        
class StatsTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('stats'), follow = True)
        self.assertEqual(response.status_code, 200) 

class UpdateSuccessTest(TestCase):
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('updatesuccess'), follow = True)
        self.assertEqual(response.status_code, 200) 
        
#Template test        
class TemplateTest(TestCase):
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'), follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')