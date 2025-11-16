from flask import render_template, request, flash, redirect
from ..forms import LoginForm
#from app import myapp_obj
from flask import current_app as myapp_obj


#login page
@myapp_obj.route('/auth/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            #ADD LOGIC HERE (like add user to database, etc)

            return redirect('/feature')
        else:
            flash('Not successful, data missing!')
            return render_template('auth/login.html', form=form)
    #this render is the FIRST render for new users
    return render_template('auth/login.html', form = form)

