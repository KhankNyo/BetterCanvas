import unittest
from werkzeug.security import generate_password_hash
from app.models import Student, Teacher

class TestStudent(unittest.TestCase):
    def test_password(self): ## doesn't work yet, still working on it


        """"
        student = Student()
        password = "password12345"
        student.set_password(password)
        self.assertIsNotNone(student.password)
        self.assertNotEqual(student.password, password)
        password = generate_password_hash(password)
        self.assertEqual(student.password, password)
        """

