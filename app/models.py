from app import g_DB as db
from werkzeug.security import generate_password_hash, check_password_hash

class Student(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique= True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique =True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Announcement(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=True)
    description = db.Column(db.String(1024), nullable=False)
    timestamp = db.Column(db.String(64), nullable=False)
