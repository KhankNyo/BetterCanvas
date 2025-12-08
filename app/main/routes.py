from flask import render_template, request, flash, redirect, session
from flask import current_app as myapp_obj
from ..forms import AnnouncementForm, CourseForm, ResourceForm, CourseSignUp
from ..models import Announcement, Student, Teacher, Course, Enrollment, Resource
from app import db_add_now, db_delete_now
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
@myapp_obj.route('/announcements', methods = ['GET', 'POST'])
def announcements():
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
                db_add_now(newPost)
                return redirect('/announcements')

        posts = Announcement.query.all()
        return render_template('main/announcements.html', username=username, isStudent=isStudent, posts=posts, form=form)

    flash('You are not logged in!')
    return redirect('/auth/login')

@myapp_obj.route('/announcements_redirect')
def announcementsRedirect():
    if "username" in session:
        flash('Moved to announcements page!')
    return redirect('/announcements')

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
        return render_template('main/people.html', username = session.get('username'), isStudent = session.get('student'), students = students, teachers = teachers)
    flash('You are not logged in!')
    return redirect('/auth/login')

@myapp_obj.route('/courses', methods = ['GET', 'POST'])
def showCourses():
    if "username" in session:
        courses = Course.query.all()
        isStudent = session.get('student')
        username = session.get('username')
	#if a teacher, make form for teachers to create a course and send it render_template
        if not isStudent: #form to get for teachers
            courseForm = CourseForm()
            name = courseForm.name.data
            desc = courseForm.description.data
            unit = courseForm.units.data
            capacity = courseForm.capacity.data
            #also have form for dropping students
            dropForm = CourseSignUp()
            #finally retrieve the teacher
            teacher = Teacher.query.filter_by(username=session.get("username")).first()

            #LOGIC: we need to retrieve the list of courses taught by professor,
            #BUT ALSO the list of students in that course (so a nested list of sorts)
            coursesTaught = Course.query.filter_by(teacher_id=teacher.id)

            if request.method == 'POST':
                #name 'course_form' is defined in jinja2 html
                if courseForm.validate_on_submit():
                    #attach current teacher's id to course just made and add it to db
                    teacher = Teacher.query.filter_by(username=session.get("username")).first()
                    newCourse = Course(name=name, description=desc, units=unit, max_capacity=capacity, teacher_id=teacher.id)
                    db_add_now(newCourse)
                    return redirect('/courses')
                elif dropForm.validate_on_submit():
                    #retrieve hidden data from request
                    course_id = request.form.get('course_id')
                    student_id = request.form.get('student_id')
                    enrollment = Enrollment.query.filter_by(student_id=student_id,course_id=course_id).first()
                    course = Course.query.filter_by(id=course_id).first()
                    course.students_enrolled -= 1
                    student = Student.query.filter_by(id=student_id).first()
                    student.units_enrolled -= course.units
                    db.session.delete(enrollment)
                    db.session.commit()
                    return redirect('/courses')

            #this is first page teacher will see
            return render_template('main/courses.html', username=username, isStudent=isStudent, courses=courses, form=courseForm, dropForm=dropForm,coursesTaught=coursesTaught)
        else: #student view - make form for students to enroll in courses instead (enroll button per course)
            enrollForm = CourseSignUp()
            #we can retrieve the student's enrollment because Student has property .enrollments that joins Student and Enrollments off the ID
            student = Student.query.filter_by(username=session.get("username")).first()
            studentEnrollments = student.enrollments
            #logic: when the 'Enroll' button is pressed, we want to get the student's id and course's id to add to Enrollments
            if request.method == 'POST':
                #the data for the course id is in the request form
                course_id = request.form.get('course_id')
                if course_id:
                    # NOTE(khanh): kinda sketchy, 'drop' button will submit a course to drop, 'enroll' button submits a None object
                    already_enrolled = Enrollment.query.filter_by(student_id=student.id, course_id=course_id).first()
                    if already_enrolled:
                        course = Course.query.filter_by(id=course_id).first()
                        #update course enrollment count and student's units
                        course.students_enrolled -= 1
                        student.units_enrolled -= course.units
                        #delete/drop already_enrolled tuple from relation Enrollment
                        db_delete_now(already_enrolled)
                        flash("Dropped the class!")
                    else:
                        course = Course.query.filter_by(id=course_id).first()
                        #check if it doesnt violate max unit allowance OR if there is no space in the class
                        if student.units_enrolled > 20:
                            flash('This course would put you over the unit limit (20). Drop another class to fit this one.')
                        elif course.students_enrolled > course.max_capacity:
                            flash('This course is at max capacity. Sorry!.')
                        else:
                            #update students units and course's enrollment count
                            course.students_enrolled += 1
                            student.units_enrolled += course.units
                            newEnroll = Enrollment(student_id=student.id, course_id=course.id)
                            db_add_now(newEnroll)
                            flash('Succesfully enrolled!')
                    return redirect('/courses')
            return render_template('main/courses.html', username=username, isStudent=isStudent, courses=courses, enrollForm = enrollForm, studentEnrollments = studentEnrollments, student=student)
    #redirect non-users to log in first
    flash('You are not logged in!')
    return redirect('/auth/login')

@myapp_obj.route("/resources", methods = ["GET", "POST", "DELETE"])
def resources():
    form = ResourceForm()
    title = form.title.data
    desc = form.description.data
    timestamp = getCurrentTime()
    if "username" in session:
        username = session.get("username")
        email = session.get("email")
        if request.method == 'POST':
            if form.validate_on_submit():
                flash ("Not yet implemented.")
                '''flash("Resource Posted!")
                newPost = Resource(title=title, description=desc, timestamp=timestamp, announcer=username, email=email)
                db.session.add(newPost)
                db.session.commit()'''
                return redirect('/resources')

        posts = Resource.query.all()

        return render_template('main/resources.html', username=username, posts=posts, form=form)
    flash('You are not logged in!')
    return redirect('/auth/login')

@myapp_obj.route('/logout')
def logout():
    return redirect("auth/signout")

def getCurrentTime():
    # NOTE(Khanh): timezones are a big and ugly mess, we'll assume the time from where the app is running
    serverTimeToday = time.ctime()
    return serverTimeToday
