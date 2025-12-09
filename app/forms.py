from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, FileField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    isTeacher = BooleanField('I am a teacher')
    submit = SubmitField('Register')

class SignOutForm(FlaskForm):
    submit = SubmitField('Sign Out')

class AnnouncementForm(FlaskForm):
     title = StringField('Title')
     description = TextAreaField('Description', validators=[DataRequired()])
     submit = SubmitField('Post')

class CourseForm(FlaskForm):
    name = StringField('Course Name', validators=[DataRequired()])
    description = TextAreaField('Course Description')
    units = IntegerField('Units Provided', validators=[DataRequired()])
    capacity = IntegerField('Maximum Students', validators=[DataRequired()])
    submit = SubmitField('Create Course')

class CourseSignUp(FlaskForm):
    submit = SubmitField('Enroll')

class ResourceForm(FlaskForm):
    title = StringField('Title')
    description = TextAreaField('Description', validators=[DataRequired()])
    file = FileField('File', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'pdf', 'txt'], 'Images, Text Documents and PDFs only!')
    ])
    submit = SubmitField('Post')

class AssignmentCreate(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    points = IntegerField('Maximum Points', validators=[DataRequired()])
    submit = SubmitField('Post Assignment')

class SubmissionForm(FlaskForm):
    file_handle = FileField('Upload File', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'pdf', 'txt'], 'Images, Text Documents and PDFs only!')
    ])
    submit = SubmitField('Submit Assignment')

class GradeForm(FlaskForm):
    score = IntegerField('Score', validators=[DataRequired()])
    submit = SubmitField('Post Submission Score')

class Button(FlaskForm):
    submit = SubmitField()
