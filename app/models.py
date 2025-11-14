from app import db

class Student(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Teacher(db.Model):
	id =  db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), nullable=False)
	password = db.Column(db.String(32), nullable=False)
	email = db.Column(db.String(100), nullable=False)

class Announcement(db.Model):
	id =  db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(32), nullable=True)
	description = db.Column(db.String(200), nullable=False)
