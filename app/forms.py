from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired

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
    description = StringField('Course Description')
    units = IntegerField('Units Provided', validators=[DataRequired()])
    submit = SubmitField('Create Course')
