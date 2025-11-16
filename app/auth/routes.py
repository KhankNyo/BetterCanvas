from flask import render_template, request, flash, redirect, session
from ..forms import LoginForm, RegistrationForm, SignOutForm
#from app import myapp_obj
from flask import current_app as myapp_obj
from ..models import Student, Teacher
from app import g_DB as db
from werkzeug.security import check_password_hash

#login page
@myapp_obj.route('/auth/login', methods = ['GET', 'POST'])
def login():
    #check if the current session is already active
    if session.get('username'):
        return redirect('/auth/signout')
    else:
        form = LoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                #ADD LOGIC HERE (like check user from database, etc)
                username= form.username.data
                password = form.password.data
		#check if the user data is in Student or Teacher tables
                isStudent = True
                user=Student.query.filter_by(username=username).first()
                if not user:
                    user=Teacher.query.filter_by(username=username).first()
                    isStudent = False

                if user and check_password_hash(user.password, password):
                    session['username'] = user.username
                    session['student'] = isStudent
                    flash('Login Successful')
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
    isTeacher = form.isTeacher.data
    user = Student.query.filter_by(username=username).first()
    if not user:
        user = Teacher.query.filter_by(username=username).first()

    if request.method == 'POST':
        if form.validate_on_submit():
            if user:
                flash('Username already taken!')
                return redirect('/auth/register')
            else:
                if isTeacher:
                    new_teacher = Teacher(username=username, email=email)
                    new_teacher.set_password(password)
                    db.session.add(new_teacher)
                    db.session.commit()
                    session['username'] = new_teacher.username
                    session['student'] = False
                else:
                    new_student = Student(username=username, email=email)
                    new_student.set_password(password)
                    db.session.add(new_student)
                    db.session.commit()
                    session['username'] = new_student.username
                    session['student'] = True
                flash('Successfully registered! You are logged in!')
                return redirect('/feature')

    return render_template('auth/register.html', form=form)

@myapp_obj.route('/auth/signout', methods = ['GET', 'POST'])
def signout():
    form = SignOutForm()
    if request.method == 'POST':
            if form.validate_on_submit():
                session.clear()
                flash('Signed Out!')
                return redirect('/auth/login')
            else:
                flash('Failed to sign out')
    #first render that client will see
    return render_template('auth/signout.html', form = form)
