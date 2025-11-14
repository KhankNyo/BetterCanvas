from flask import render_template
from .forms import LoginForm
#from app import myapp_obj
from flask import current_app as myapp_obj

@myapp_obj.route('/')
# view functions
def hello():
    return '<h1>hello world</h1>'

# http://127.0.0.1:5000/members/Carlos/
@myapp_obj.route('/members/<string:naame>/')
def member(naame):
    return naame

@myapp_obj.route('/morn')
def morning():
    return 'Good Morning!'

@myapp_obj.route('/login')
def login():
    form = LoginForm()
    abc = {'name':'carlos'}
    return render_template('login.html', users=abc, form=form)

