from flask import render_template, request, flash, redirect
from .forms import LoginForm
#from app import myapp_obj
from flask import current_app as myapp_obj

#home page that shows links in our site
@myapp_obj.route('/')
def index():
    return render_template('index.html')
#LOGIC: in index.html, the links go to redirects so I can flash a message
@myapp_obj.route('/redirect')
def indexRedirect():
    flash('You''re already here!')
    return redirect('/')


#demo page to still work on
@myapp_obj.route('/feature')
def newFeature():
    return render_template('features.html')
@myapp_obj.route('/feature_redirect')
def newFeatureRedirect():
    flash('Moved to announcements page!')
    return redirect('/feature')

#login page
@myapp_obj.route('/auth/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash('Succesfully logged in!')
            #ADD LOGIC HERE (like add user to database, etc)
            return redirect('/feature')
        else:
            flash('Not successful, data missing!')
            return render_template('login.html', form=form)
    #this render is the FIRST render for new users
    return render_template('login.html', form = form)
@myapp_obj.route('/login_redirect')
def loginRedirect():
    flash('Moved to login page!')
    return redirect('/auth/login')
