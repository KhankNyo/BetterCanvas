from app import g_DB as db
from werkzeug.security import generate_password_hash, check_password_hash

g_EMAIL_STRING_CAPACITY = 128
g_NAME_STRING_CAPACITY = 64
g_PASSWORD_STRING_CAPACITY = 64

class Student(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(g_NAME_STRING_CAPACITY), unique= True, nullable=False)
    password = db.Column(db.String(g_PASSWORD_STRING_CAPACITY), nullable=False)
    email = db.Column(db.String(g_EMAIL_STRING_CAPACITY), nullable=False)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(g_NAME_STRING_CAPACITY), unique =True, nullable=False)
    password = db.Column(db.String(g_PASSWORD_STRING_CAPACITY), nullable=False)
    email = db.Column(db.String(g_EMAIL_STRING_CAPACITY), nullable=False)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Announcement(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(1024), nullable=False)
    timestamp = db.Column(db.String(64), nullable=False)
    announcer = db.Column(db.String(g_NAME_STRING_CAPACITY), nullable=False)
    email = db.Column(db.String(g_EMAIL_STRING_CAPACITY), nullable=False)
