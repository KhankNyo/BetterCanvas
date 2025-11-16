from flask import render_template, request, flash, redirect
from ..forms import LoginForm
#from app import myapp_obj
from flask import current_app as myapp_obj

from ..models import Student


#login page
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
                return redirect('/feature')
            else:
                flash('Not successful, data missing or incorrect!')
                return redirect('/auth/login')
    #this render is the FIRST render for new users
    return render_template('auth/login.html', form = form)

