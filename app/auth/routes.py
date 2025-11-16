from flask import render_template, request, flash, redirect, session
from ..forms import LoginForm, RegistrationForm
from flask import current_app as myapp_obj
from ..models import Student
from app import g_DB as db
from werkzeug.security import check_password_hash
import flask_login

@myapp_obj.route('/auth/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            #ADD LOGIC HERE (like add user to database, etc)
            username= form.username.data
            password = form.password.data
            user=Student.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                flash('Login Successful')
                session['username'] = username
                return redirect('/feature')
            else:
                flash('Not successful, data missing or incorrect!')
                return redirect('/auth/login')
    #this render is the FIRST render for new users
    return render_template('auth/login.html', form = form)

@myapp_obj.route('/auth/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    username = form.username.data
    password = form.password.data
    email = form.email.data
    user = Student.query.filter_by(username=username).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            if user:
                flash('Username already taken!')
                return redirect('/auth/register')
            else:
                new_student = Student(username=username, email=email)
                new_student.set_password(password)
                db.session.add(new_student)
                db.session.commit()
                flash('Successfully registered! You are now logged in!')
                return redirect('/feature')

    return render_template('auth/register.html', form=form)