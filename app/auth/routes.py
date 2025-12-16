from flask import request, flash, redirect, session
#from flask import current_app as myapp_obj
from ..forms import LoginForm, RegistrationForm, SignOutForm
from ..models import Student, Teacher
from ..session import *
#from app import db_add_now, app_render_template
from werkzeug.security import check_password_hash
import flask_login


def init_auth_routes(myapp_obj):
    from app import db_add_now, app_render_template

    @myapp_obj.route('/auth/login', methods = ['GET', 'POST'])
    def login():
        if session_is_current_user_logged_in():
            flash('You are already logged in.')
            return redirect('/')

        form = LoginForm()
        if request.method == 'POST' and form.validate_on_submit():
            #ADD LOGIC HERE (like check user from database, etc)
            userdata, user = session_find_user_by_name(form.username.data)
            if not user:
                flash(f'No user named \'{form.username.data}\', perhaps you wanted to sign in?')
                return redirect('/auth/login')

            if not check_password_hash(user.password, form.password.data):
                flash('Wrong password, try again.')
                return redirect('/auth/login')

            session_update_current_user(userdata)
            flash('Login Successful')
            return redirect('/announcements')

        #this render is the FIRST render for new users
        return app_render_template('auth/login.html', form = form)


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
                        db_add_now(new_teacher)
                        session_add_current_user_locally(name=username, is_student=False, email=email)
                    else:
                        new_student = Student(username=username, email=email)
                        new_student.set_password(password)
                        db_add_now(new_student)
                        session_add_current_user_locally(name=username, is_student=True, email=email)
                    flash('Successfully registered! You are logged in!')
                    return redirect('/announcements')

        return app_render_template('auth/register.html', form=form)

    @myapp_obj.route('/auth/signout', methods = ['GET'])
    def signout():
        if not session_is_current_user_logged_in():
            flash('You are not logged in.')
        else:
            session_remove_current_user()
            flash('You are now logged out.')
        return redirect('/')

