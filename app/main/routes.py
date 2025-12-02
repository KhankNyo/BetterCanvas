from flask import render_template, request, flash, redirect, session
from flask import current_app as myapp_obj
from ..forms import AnnouncementForm, CourseForm
from ..models import Announcement, Student, Teacher, Course, Enrollment
from app import g_DB as db
import time, sqlite3

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
    form = AnnouncementForm()
    title = form.title.data
    desc = form.description.data
    timestamp = getCurrentTime()

    if "username" in session:
        username = session.get("username")
        isStudent = session.get("student")
        email = session.get("email")

        if request.method == 'POST':
            if form.validate_on_submit():
                flash("Post announced!")
                newPost = Announcement(title=title, description=desc, timestamp=timestamp, announcer=username, email=email)
                db.session.add(newPost)
                db.session.commit()
                return redirect('/feature')

        posts = Announcement.query.all()
        return render_template('main/features.html', username=username, isStudent=isStudent, posts=posts, form=form)

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
        teachers = Teacher.query.all()
        students = Student.query.all()
        return render_template('people.html', username = session.get('username'), isStudent = session.get('student'), students = students, teachers = teachers)
    flash('You are not logged in!')
    return redirect('/auth/login')

@myapp_obj.route('/courses', methods = ['GET', 'POST'])
def createCourse():
    if "username" in session:
        courses = Course.query.all()
        isStudent = session.get('student')
        username = session.get('username')
        if not isStudent: #form to get for teachers
            form = CourseForm()
            name = form.name.data
            desc = form.description.data
            unit = form.units.data

            if request.method == 'POST':
                if form.validate_on_submit():
                    #attach current teacher's id to course just made and add it to db
                    teacher = Teacher.query.filter_by(username=session.get("username")).first()
                    newCourse = Course(name=name, description=desc, units=unit, teacher_id=teacher.id)
                    db.session.add(newCourse)
                    db.session.commit()
                    return redirect('/courses')
            #this is first page teacher will see
            return render_template('main/courses.html', username=username, isStudent=isStudent, courses=courses, form=form)
        else: #student view
            return render_template('main/courses.html', username=username, isStudent=isStudent, courses=courses)
    #redirect non-users to log in first
    flash('You are not logged in!')
    return redirect('/auth/login')

@myapp_obj.route('/logout')
def logout():
    return redirect("auth/signout")


def getCurrentTime():
    # NOTE(Khanh): timezones are a big and ugly mess, we'll assume the time from where the app is running
    serverTimeToday = time.ctime()
    return serverTimeToday
