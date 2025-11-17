from flask import render_template, request, flash, redirect, session
from flask import current_app as myapp_obj
from ..forms import AnnouncementForm
from ..models import Announcement
from app import g_DB as db
import time

#home page that shows links in our site
@myapp_obj.route('/')
def index():
    return render_template('main/index.html', username = session.get('username'), isStudent = session.get('student'))

#LOGIC: in index.html, the links go to redirects so I can flash a message
@myapp_obj.route('/redirect')
def indexRedirect():
    flash('You\'re already here!')
    return redirect('/')

#demo page to still work on
@myapp_obj.route('/feature', methods = ['GET', 'POST'])
def newFeature():
    posts = Announcement.query.all()
    form = AnnouncementForm()
    title = form.title.data
    desc = form.description.data
    timestamp = getCurrentTime();
    if "username" in session:
        if request.method == 'POST':
            if form.validate_on_submit():
                flash("Post announced!")
                newPost = Announcement(title=title, description=desc, timestamp=timestamp)
                db.session.add(newPost)
                db.session.commit()
                return redirect('/feature')

        return render_template('main/features.html', username=session.get('username'), isStudent=session.get('student'),
                               posts=posts, form=form)
    flash('You are not logged in!')
    return redirect('/auth/login')

@myapp_obj.route('/feature_redirect')
def newFeatureRedirect():
    if "username" in session:
        flash('Moved to announcements page!')
    return redirect('/feature')

@myapp_obj.route('/login_redirect')
def loginRedirect():
    if session.get('username'):
        flash('You are already logged in.')
        return redirect('/')
    else:
        flash('Moved to login page!')
        return redirect('/auth/login')

@myapp_obj.route('/people')
def people():
    #list out people in the class and their contact info. get it from database
    if "username" in session:
        return render_template('people.html', username = session.get('username'), isStudent = session.get('student'))
    flash('You are not logged in!')
    return redirect('/auth/login')

@myapp_obj.route('/postcreated')
def postRedirect():
    flash('Created Post (not implemented yet)!')
    return redirect('/feature')

@myapp_obj.route('/logout')
def logout():
    return redirect("auth/signout")


def getCurrentTime():
    # NOTE: timezones are aa big and ugly mess, we'll assume the time from where the app is running
    serverTimeToday = time.ctime()
    print(serverTimeToday)
    return serverTimeToday
