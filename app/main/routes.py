from flask import render_template, request, flash, redirect
#from app import myapp_obj
from flask import current_app as myapp_obj
from ..forms import LoginForm

#home page that shows links in our site
@myapp_obj.route('/')
def index():
    return render_template('main/index.html')

#LOGIC: in index.html, the links go to redirects so I can flash a message
@myapp_obj.route('/redirect')
def indexRedirect():
    flash('You''re already here!')
    return redirect('/')

#demo page to still work on
@myapp_obj.route('/feature')
def newFeature():
    return render_template('main/features.html')

@myapp_obj.route('/feature_redirect')
def newFeatureRedirect():
    flash('Moved to announcements page!')
    return redirect('/feature')

@myapp_obj.route('/login_redirect')
def loginRedirect():
    flash('Moved to login page!')
    return redirect('/auth/login')
