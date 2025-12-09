from app import g_DB as db
from werkzeug.security import generate_password_hash, check_password_hash

g_EMAIL_STRING_CAPACITY = 128
g_NAME_STRING_CAPACITY = 64
g_PASSWORD_STRING_CAPACITY = 64
g_DESCRIPTION_STRING_CAPACITY = 1024
g_TIMESTAMP_STRING_CAPACITY = 64

class Student(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(g_NAME_STRING_CAPACITY), unique= True, nullable=False)
    password = db.Column(db.String(g_PASSWORD_STRING_CAPACITY), nullable=False)
    email = db.Column(db.String(g_EMAIL_STRING_CAPACITY), nullable=False)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    units_enrolled = db.Column(db.Integer, default = 0)
    #relationships
    enrollments = db.relationship('Enrollment', backref="students")
    submissions = db.relationship('Submission', backref="students")

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
    title = db.Column(db.String(g_NAME_STRING_CAPACITY), nullable=True)
    description = db.Column(db.String(g_DESCRIPTION_STRING_CAPACITY), nullable=False)
    timestamp = db.Column(db.String(g_TIMESTAMP_STRING_CAPACITY), nullable=False)
    announcer = db.Column(db.String(g_NAME_STRING_CAPACITY), nullable=False)
    email = db.Column(db.String(g_EMAIL_STRING_CAPACITY), nullable=False)

class Resource(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(g_NAME_STRING_CAPACITY), nullable=True)
    description = db.Column(db.String(g_DESCRIPTION_STRING_CAPACITY), nullable=False)
    file = db.Column(db.String(g_NAME_STRING_CAPACITY), nullable=False)
    timestamp = db.Column(db.String(g_TIMESTAMP_STRING_CAPACITY), nullable=False)
    announcer = db.Column(db.String(g_NAME_STRING_CAPACITY), nullable=False)
    email = db.Column(db.String(g_EMAIL_STRING_CAPACITY), nullable=False)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(g_NAME_STRING_CAPACITY), nullable=False)
    description = db.Column(db.String(g_DESCRIPTION_STRING_CAPACITY), nullable = True)
    units = db.Column(db.Integer, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    students_enrolled = db.Column(db.Integer, default=0)
    #foreign key ensures data integrity: a course cannot be added with a
    #teacherID that does not exist in Teacher table first
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=False)
    #this is to define a reference to Teacher table and Enrollment table (ex: using myCourse.teacher.name)
    #i.e. relationships
    teacher = db.relationship('Teacher', backref='courses')
    enrollments = db.relationship("Enrollment", backref="courses")
    assignments = db.relationship("Assignment", backref='courses')

class Enrollment(db.Model):
    #this table uses TWO foreign keys as a composite key
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), primary_key=True)
    course_grade = db.Column(db.Float, default = 0.00)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    description = db.Column(db.String(g_DESCRIPTION_STRING_CAPACITY), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    submissions = db.relationship("Submission", backref="assignments")

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"))
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    file_handle = db.Column(db.String(255), nullable=False)
    points_given = db.Column(db.Integer, default = 0)
