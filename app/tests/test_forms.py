import unittest, pytest
from flask import Flask
from app.forms import LoginForm, RegistrationForm, AnnouncementForm

class TestLoginForm(unittest.TestCase): #test if user is able to login and if the login form is using the right information
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['WTF_CSRF_ENABLED'] = False

    def test_valid_login(self):
        with self.app.test_request_context(method= 'POST', data = {'username': 'tester','password': 'password123', 'remember_me': 'y'}):
            form = LoginForm()
            self.assertTrue(form.validate_on_submit())
            self.assertEqual(form.username.data, 'tester')
            self.assertEqual(form.password.data, 'password123')
            self.assertTrue(form.remember_me.data)
    def test_invalid_login(self):
        with self.app.test_request_context(method='POST', data = {'username': 'tester',}):
            form = LoginForm()
            self.assertFalse(form.validate_on_submit())

class TestRegistrationForm(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['WTF_CSRF_ENABLED'] = False

    def test_valid_registration(self):
        with self.app.test_request_context(method='POST', data = {'username': 'teacher','password': 'password123',
                                                                  'email': 'teacher@email.com', 'isTeacher': True}):
            form = RegistrationForm()
            self.assertTrue(form.validate_on_submit())
            self.assertEqual(form.username.data, 'teacher')
            self.assertEqual(form.password.data, 'password123')
            self.assertTrue(form.email.data)
            self.assertTrue(form.isTeacher.data)

    def test_invalid_registration(self):
        with self.app.test_request_context(method='POST', data = {'password': 'password123',}):
            form = RegistrationForm()
            self.assertFalse(form.validate_on_submit())

class TestAnnouncement(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['WTF_CSRF_ENABLED'] = False

    def test_valid_registration(self):
        with self.app.test_request_context(method='POST', data = {'title': 'TITLE','description': 'This is a description'}):
            form = AnnouncementForm()
            self.assertTrue(form.validate_on_submit())
            self.assertEqual(form.title.data, 'TITLE')
            self.assertEqual(form.description.data, 'This is a description')
    def test_invalid_registration(self):
        with self.app.test_request_context(method='POST', data = {'title': 'TITLE',}):
            form = AnnouncementForm()
            self.assertFalse(form.validate_on_submit())
