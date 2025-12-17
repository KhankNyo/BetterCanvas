from flask import request, flash, redirect, session, url_for, send_from_directory
#from flask import current_app as myapp_obj
from ..forms import AnnouncementForm, CourseForm, ResourceForm, CourseSignUp, AssignmentCreate, Button, SubmissionForm, GradeForm
from ..models import Announcement, Student, Teacher, Course, Enrollment, Resource, Assignment, Submission
from ..session import *
from app import db_add_now, db_delete_now, db_commit, app_render_template
from werkzeug.utils import secure_filename
import time, sqlite3, os

# BUG:(khanh): When the user does not exist in the db but logged in (cached by browser), the app crashes attempting to retreive the user's info from the DB

def init_main_routes(myapp_obj):
    #home page that shows links in our site
    @myapp_obj.route('/', methods = ['GET', 'POST'])
    def index():
        return redirect('/announcements')

    #LOGIC: in index.html, the links go to redirects so I can flash a message
    @myapp_obj.route('/redirect')
    def indexRedirect():
        flash('You\'re already here!')
        return redirect('/')

    @myapp_obj.route('/announcements', methods = ['GET', 'POST'])
    def announcements():
        print(f"DEBUG(ROUTE): {dict(session)}") #this is for testing purposes
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
            return app_render_template('main/announcements.html', username=username, isStudent=isStudent, posts=posts, form=form)

        flash('You are not logged in!')
        return redirect('/auth/login')

    @myapp_obj.route('/courses/create', methods = ['GET', 'POST'])
    def promptCourseCreation():
        if not session_is_current_user_logged_in():
            return forceUserToLogIn()

        user = session_get_current_user_obj()
        assert(user.type == UserType.TEACHER and "BAD BAD BAD, only teacher can have access to course creation form")

        courseCreationForm = CourseForm()
        if request.method == 'POST':
            if courseCreationForm.validate_on_submit():
                # NOTE:(khanh): user filled out course creation form, add it to db
                newCourse = Course(
                    name=user.name, 
                    description=courseCreationForm.description.data, 
                    units=courseCreationForm.units.data, 
                    max_capacity=courseCreationForm.capacity.data, 
                    teacher_id=user.id
                )
                # TODO:(khanh): update course list in userobj
                db_add_now(newCourse)
                return redirect('/courses')
            else:
                # NOTE:(khanh): incorrect fields, log this? 
                dummyNopFn()
        else:
            # NOTE:(khanh): GET or other methods, log this?
            dummyNopFn()
        return app_render_template('main/courses_create.html', form=courseCreationForm)

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
            return app_render_template('main/people.html', username = session.get('username'), isStudent = session.get('student'), students = students, teachers = teachers)
        flash('You are not logged in!')
        return redirect('/auth/login')

    @myapp_obj.route('/courses', methods = ['GET', 'POST'])
    def showCoursesPage():
        return showCoursesImpl(isAtHomePage=False)

    #@myapp_obj.route('/courses', methods = ['GET', 'POST'])
    def showCoursesImpl(isAtHomePage):
        templateName = "main/courses.html"
        if isAtHomePage:
            templateName = "main/index.html"

        if "username" in session:
            courses = Course.query.all()
            isStudent = session.get('student')
            username = session.get('username')
            #if a teacher, make form for teachers to create a course and send it app_render_template
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
                        student = Student.query.filter_by(id=student_id).first()
                        course.students_enrolled -= 1
                        student.units_enrolled -= course.units
                        db_delete_now(enrollment);
                        return redirect('/courses')

                #this is first page teacher will see
                return app_render_template(templateName, username=username, isStudent=isStudent, courses=courses, form=courseForm, dropForm=dropForm, coursesTaught=coursesTaught)
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
                        # NOTE:(khanh): kinda sketchy, 'drop' button will submit a course to drop, 'enroll' button submits a None object
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
                #first page students will see
                return app_render_template(templateName, username=username, isStudent=isStudent, courses=courses, enrollForm = enrollForm, studentEnrollments = studentEnrollments, student=student)

        #redirect non-users to log in first
        flash('You are not logged in!')
        return redirect('/auth/login')

    @myapp_obj.route("/resources", methods = ['GET', 'POST'])
    def resources():
        form = ResourceForm()
        if "username" in session:
            isStudent = session.get("student")
            username = session.get("username")
            email = session.get("email")
            if request.method == 'POST':
                if form.validate_on_submit():
                    #store the file on the app
                    fileData = form.file.data
                    fileName = secure_filename(fileData.filename)
                    filePath = os.path.join(myapp_obj.config['RESOURCES'], fileName)
                    fileData.save(filePath)
                    #store the file handle on the db
                    title = form.title.data
                    desc = form.description.data
                    timestamp = getCurrentTime()
                    newResource = Resource(title=title,description=desc,file=fileName,timestamp=timestamp,announcer=username,email=email)
                    db_add_now(newResource)
                    flash('Resource posted! Thank you for providing!')
                    return redirect('/resources')
                else:
                    print(form.errors)

            posts = Resource.query.all()

            return app_render_template('main/resources.html', username=username, posts=posts, form=form, isStudent=isStudent)
        flash('You are not logged in!')
        return redirect('/auth/login')

    @myapp_obj.route('/logout')
    def logout():
        return redirect("auth/signout")

    @myapp_obj.route('/assignments', methods = ['GET', 'POST'])
    def assignments():
        if "username" in session:
            isStudent = session.get('student')
            #LOGIC: for students, show each course - show assignments and give a form to submit a file to assignment
            #       for teachers, show each course - for each course give a form to create assignments.
            if isStudent:
                student = Student.query.filter_by(username=session.get("username")).first()
                studentEnrolls = student.enrollments
                course_ids = [enrollment.course_id for enrollment in studentEnrolls]
                courses = Course.query.filter(Course.id.in_(course_ids)).all()
                submission = SubmissionForm()

                if request.method == 'POST':
                    if submission.validate_on_submit():
                        #store the file on the app
                        fileData = submission.file_handle.data
                        fileName = secure_filename(fileData.filename)
                        filePath = os.path.join(myapp_obj.config['UPLOADS'], fileName)
                        fileData.save(filePath)
                        #store the file handle on the db
                        assignment_id = request.form.get('assignment_id')
                        newSubmission = Submission(assignment_id=assignment_id, student_id=student.id, file_handle=fileName, points_given=0)
                        db_add_now(newSubmission)
                        flash('Congratulations, you\'ve submitted an assignment. Check back after the instructor has graded it!')
                        return redirect('/assignments')

                username = session.get('username')
                return app_render_template('main/assignments.html', courses=courses, submissionForm=submission, isStudent=isStudent, username=username)

            else:
                teacher = Teacher.query.filter_by(username=session.get("username")).first()
                courses = Course.query.filter_by(teacher_id=teacher.id)
                createForm = AssignmentCreate()

                if request.method == 'POST':
                    #create a new assignment for the course_id (retrieved by hidden tag in course)
                    desc = createForm.description.data
                    points = createForm.points.data
                    course_id = request.form.get('course_id')
                    if course_id:
                        # nice
                        newAss = Assignment(course_id=course_id, description=desc, points=points)
                        db_add_now(newAss)
                        flash('New assignment has been posted!')
                        return redirect('/assignments')

                username = session.get('username')
                return app_render_template('main/assignments.html', courses=courses, assignmentForm=createForm, isStudent=isStudent, username=username)

        #redirect non-users to log in first
        flash('You are not logged in!')
        return redirect('/auth/login')

    @myapp_obj.route('/submissions', methods = ['GET', 'POST'])
    def submissions():
        if "username" in session:
            isStudent = session.get('student')
            #LOGIC: for students, they shouldnt be here. This is purely so that professors can grade their submissions
            #       for teachers, show each course - for each course show the list of posted submissions. Give a form to submit a grade
            if isStudent:
                return redirect('/assignments')
            else:
                #Submission has an assignment_id. From assignment_id we can link it to a course. So course --> assignment --> submissions
                teacher = Teacher.query.filter_by(username=session.get("username")).first()
                courses = Course.query.filter_by(teacher_id=teacher.id)
                gradingForm = GradeForm()

                if request.method == 'POST':
                    if gradingForm.validate_on_submit():
                        #get the score data, plus grab the student and course id's from the request (so we can calculate the course_grade)
                        newScore = gradingForm.score.data
                        submission_id = request.form.get('submission_id')
                        student_id = request.form.get('student_id')
                        course_id = request.form.get('course_id')
                        if course_id:
                            submissionToUpdate = Submission.query.filter_by(id=submission_id).first()
                            student = Student.query.filter_by(id=student_id).first()
                            course = Course.query.filter_by(id=course_id).first()
                            submissionToUpdate.points_given = newScore
                            calculateStudentGrade(student, course)
                            db_commit()
                            flash('New score has been submitted.')
                            return redirect('/submissions')

                username = session.get('username')
                return app_render_template('main/submissions.html', courses=courses, form=gradingForm, username=username)

        #redirect non-users to log in first
        flash('You are not logged in!')
        return redirect('/auth/login')

    #dynamic route that sends links to uploaded files
    @myapp_obj.route('/uploads/<filename>')
    def uploadedFile(filename):
        uploadFolder = myapp_obj.config['UPLOADS']
        return send_from_directory(uploadFolder, filename)

    #dynamic route that sends links to resource files
    @myapp_obj.route('/resources/<filename>')
    def resourceFile(filename):
        resourceFolder = myapp_obj.config['RESOURCES']
        return send_from_directory(resourceFolder, filename)

    def getCurrentTime():
        # NOTE:(Khanh): timezones are a big and ugly mess, we'll assume the time from where the app is running
        serverTimeToday = time.ctime()
        return serverTimeToday

    def calculateStudentGrade(student, course):
        #LOGIC: sum up the points for course in one variable, sum up the score of the course in another. Grade = score/coursePoints
        score = 0
        coursePoints = 0
        courseAssignments = course.assignments
        for assignment in courseAssignments:
            #retrieve submission and increment values
            submission = Submission.query.filter_by(assignment_id=assignment.id, student_id=student.id).first()
            score += submission.points_given
            coursePoints += assignment.points
        rawGrade = (score/coursePoints)*100
        formatGrade = "{:.2f}".format(rawGrade)
        #now update the student's course grade with it (exists in Enrollment table)
        enrollment = Enrollment.query.filter_by(course_id=course.id, student_id=student.id).first()
        enrollment.course_grade = formatGrade #all done!

    def forceUserToLogIn():
        flash('You are not logged in!')
        return redirect('/auth/login')

    def dummyNopFn():
        return
