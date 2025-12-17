from werkzeug.security import generate_password_hash
from app.models import Student, Teacher, Course, Enrollment, UserType, UserData, Submission, Assignment
from app.session import session_find_user_by_name, session_update_current_user
from app import g_DB as db
from flask import get_flashed_messages, session
import pytest, io, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUBMISSION_DIR = os.path.join(BASE_DIR, "assets")

def test_teacherCreatesAnnouncement_studentReadsAnnouncment(client):
    #fixture starts with empty DB so lets create the users
    hashed_passStudent = generate_password_hash("ILikeTurtles")
    student = Student(username="JohnDoe", password=hashed_passStudent, email="john@sample.com")
    hashed_passTeacher = generate_password_hash("IAmATeacher")
    teacher = Teacher(username="MathProfessor", password=hashed_passTeacher, email="mathiscool@coolmathgames.com")
    with client.application.app_context(): #need this context whenever accessing the database
        db.session.add(student)
        db.session.add(teacher)
        db.session.commit()

    #teacher is logged in so we have two pieces of data stored in session: "username"(String) and "student"(boolean)
    with client.application.app_context():
        if session_find_user_by_name("MathProfessor"):
            userdata, user = session_find_user_by_name("MathProfessor")
        else:
            print("Could not find user")

    print(f"DEBUG: {userdata.name}") #this is for testing purposes

    with client.application.test_request_context('/'):
        with client.session_transaction() as sess:

            sess['userobj'] = userdata.as_dict()
            sess['username'] = userdata.name
            sess['student'] = userdata.type == UserType.STUDENT
            sess['email'] = userdata.email
            sess.modified = True

    rv = client.get('/announcements', follow_redirects=False)    
    assert rv.status_code == 200
    html_content = rv.get_data(as_text=True) #big string
    #NOTE (Bryan): I have to separate string assertions because of hidden whitespace characters in jinja2 html templates
    assert "Logged in as " in html_content
    assert "teacher: " in html_content
    assert "MathProfessor" in html_content

    ## CREATE THE ANNOUNCEMENT ##
    rv = client.post('/announcements', data = {
        'title': 'This is a new post',
        'description': 'With a new description'
    }, follow_redirects=True)

    #verify the teacher can see it
    assert rv.status_code == 200
    html_content = rv.get_data(as_text=True) #big string
    assert "This is a new post" in html_content
    assert "With a new description" in html_content

    # now lets switch to the student and see if they can see the announcement
    with client.application.app_context():
        if session_find_user_by_name("JohnDoe"):
            userdata, user = session_find_user_by_name("JohnDoe")
        else:
            print("Could not find user")
    print(f"DEBUG: {userdata.name}") #this is for testing purposes
    with client.application.test_request_context('/'):
        with client.session_transaction() as sess:
            sess['userobj'] = userdata.as_dict()
            sess['username'] = userdata.name
            sess['student'] = userdata.type == UserType.STUDENT
            sess['email'] = userdata.email
            sess.modified = True

    #verify student is logged in and can see the new announcement
    rv = client.get('/announcements', follow_redirects=False)
    assert rv.status_code == 200
    html_content = rv.get_data(as_text=True) #big string
    assert "Logged in as " in html_content
    assert "student: " in html_content
    assert "JohnDoe" in html_content
    assert "This is a new post" in html_content
    assert "With a new description" in html_content


def test_teacherCreatesCourse_studentEnrollsCourse(client):
    #fixture starts with empty DB so lets create the users
    hashed_passStudent = generate_password_hash("ILikeTurtles")
    student = Student(username="JohnDoe", password=hashed_passStudent, email="john@sample.com")
    hashed_passTeacher = generate_password_hash("IAmATeacher")
    teacher = Teacher(username="MathProfessor", password=hashed_passTeacher, email="mathiscool@coolmathgames.com")
    with client.application.app_context(): #need this context whenever accessing the database
        db.session.add(student)
        db.session.add(teacher)
        db.session.commit()

    #teacher is logged in so we have two pieces of data stored in session: "username"(String) and "student"(boolean)
    with client.application.app_context():
        if session_find_user_by_name("MathProfessor"):
            userdata, user = session_find_user_by_name("MathProfessor")
        else:
            print("Could not find user")

    print(f"DEBUG: {userdata.name}") #this is for testing purposes

    with client.application.test_request_context('/'):
        with client.session_transaction() as sess:

            sess['userobj'] = userdata.as_dict()
            sess['username'] = userdata.name
            sess['student'] = userdata.type == UserType.STUDENT
            sess['email'] = userdata.email
            sess.modified = True

    rv = client.get('/announcements', follow_redirects=False)
    assert rv.status_code == 200
    html_content = rv.get_data(as_text=True) #big string
    #NOTE (Bryan): I have to separate string assertions because of hidden whitespace characters in jinja2 html templates
    assert "Logged in as " in html_content
    assert "teacher: " in html_content
    assert "MathProfessor" in html_content

    ## CREATE THE COURSE ##
    rv = client.post('/courses', data = {
        'name': 'Algebra II',
        'description': 'All about algebra!',
        'units': 3,
        'capacity': 27
    }, follow_redirects=True)

    #verify the teacher can see it
    assert rv.status_code == 200
    html_content = rv.get_data(as_text=True) #big string
    assert "Algebra II" in html_content
    assert "All about algebra!" in html_content
    assert "3" in html_content
    assert "27" in html_content

    # now lets switch to the student and see if they can see the just posted course
    with client.application.app_context():
        if session_find_user_by_name("JohnDoe"):
            userdata, user = session_find_user_by_name("JohnDoe")
        else:
            print("Could not find user")
    print(f"DEBUG: {userdata.name}") #this is for testing purposes
    with client.application.test_request_context('/'):
        with client.session_transaction() as sess:
            sess['userobj'] = userdata.as_dict()
            sess['username'] = userdata.name
            sess['student'] = userdata.type == UserType.STUDENT
            sess['email'] = userdata.email
            sess.modified = True

    #verify student is logged in and can see the new course
    rv = client.get('/courses', follow_redirects=True)
    assert rv.status_code == 200
    html_content = rv.get_data(as_text=True) #big string
    assert "Logged in as " in html_content
    assert "student: " in html_content
    assert "JohnDoe" in html_content
    assert "Algebra II" in html_content
    assert "All about algebra!" in html_content
    assert "3" in html_content
    assert "27" in html_content
    assert "Enroll" in html_content

    #post data for student to enroll in course
    ## ENROLL IN COURSE ##
    #since there exists the possibility of multiple courses, the data for course_id is actually inside of the html
    #we'll just retrieve the course_id manually by querying the database for "Algebra II"
    with client.application.app_context():
        algebra = Course.query.filter_by(name="Algebra II").first()
        idToPass = algebra.id

    rv = client.post('/courses', data = {"course_id" : idToPass}, follow_redirects=True)

    #verify student has an enrollment now with the right attributes
    with client.application.app_context():
        if session_find_user_by_name("JohnDoe"):
            userdata, user = session_find_user_by_name("JohnDoe")
        else:
            pytest.fail("Could not find John")

        db.session.refresh(user) #this is needed to sync database changes to the session
        enrollment_list = user.enrollments
        if not enrollment_list:
            pytest.fail("User John Doe does not have any enrollments.")

        test_enroll = enrollment_list[0]
        course = Course.query.filter_by(id = test_enroll.course_id).first()
        assert course.name == "Algebra II"
        assert course.description == "All about algebra!"
        assert course.units == 3
        assert course.max_capacity == 27


def test_teacherCreatesAssignment_studentSubmitsAssignment(client):
    #fixture starts with empty DB so lets create the users AND courses (plus states like student enrolls)
    with client.application.app_context(): #need this context whenever accessing the database
        hashed_passStudent = generate_password_hash("ILikeTurtles")
        student = Student(username="JohnDoe", password=hashed_passStudent, email="john@sample.com")        
        db.session.add(student)
        hashed_passTeacher = generate_password_hash("IAmATeacher")
        teacher = Teacher(username="MathProfessor", password=hashed_passTeacher, email="mathiscool@coolmathgames.com")
        db.session.add(teacher)
        db.session.commit() #need to commit Teacher and Student NOW bc of foreign key dependencies in Course (teacher_id)
        newCourse = Course(name="Algebra II", description="All about algebra!", units=3, max_capacity=27, teacher_id=teacher.id)
        db.session.add(newCourse)
        db.session.commit() #need to commit Course NOW bc of foreign key dependency in Enroll (course_id)
        newEnroll = Enrollment(course_id=newCourse.id, student_id=student.id, course_grade=0.00)
        db.session.add(newEnroll)
        db.session.commit()

    #teacher is logged in so we have two pieces of data stored in session: "username"(String) and "student"(boolean)
    with client.application.app_context():
        if session_find_user_by_name("MathProfessor"):
            userdata, user = session_find_user_by_name("MathProfessor")
        else:
            print("Could not find user")

    print(f"DEBUG: {userdata.name}") #this is for testing purposes

    with client.application.test_request_context('/'):
        with client.session_transaction() as sess:

            sess['userobj'] = userdata.as_dict()
            sess['username'] = userdata.name
            sess['student'] = userdata.type == UserType.STUDENT
            sess['email'] = userdata.email
            sess.modified = True

    rv = client.get('/assignments', follow_redirects=True)
    assert rv.status_code == 200
    html_content = rv.get_data(as_text=True) #big string
    #NOTE (Bryan): I have to separate string assertions because of hidden whitespace characters in jinja2 html templates
    assert "Logged in as " in html_content
    assert "teacher: " in html_content
    assert "MathProfessor" in html_content
    assert "Create a New Assignment for this course:" in html_content

    ## CREATE THE ASSIGNMENT ##
    with client.application.app_context():
        courseToAddAssTo = Course.query.filter_by(name="Algebra II").first()
        courseIdToPass = courseToAddAssTo.id
    rv = client.post('/assignments', data = {
        'description': 'Solve for x:   3x + 4 = 13',
        'points': 5,
        'course_id': courseIdToPass
    }, follow_redirects=True)

    #verify the teacher can see it
    assert rv.status_code == 200
    html_content = rv.get_data(as_text=True) #big string
    assert "Solve for x:   3x + 4 = 13" in html_content
    assert "5" in html_content
    #veify its in the database
    with client.application.app_context():
        assToCheck = Assignment.query.filter_by(description="Solve for x:   3x + 4 = 13").first()
        if assToCheck:
            assert assToCheck.points == 5
        else:
            allAsses = Assignment.query.all()
            for ass in allAsses:
                print(ass.description)
                print(ass.points)
            pytest.fail("Didn't add Assignment to the database")

    # now lets switch to the student and see if they can see the just posted assignment
    with client.application.app_context():
        if session_find_user_by_name("JohnDoe"):
            userdata, user = session_find_user_by_name("JohnDoe")
        else:
            print("Could not find user")
    print(f"DEBUG: {userdata.name}") #this is for testing purposes
    with client.application.test_request_context('/'):
        with client.session_transaction() as sess:
            sess['userobj'] = userdata.as_dict()
            sess['username'] = userdata.name
            sess['student'] = userdata.type == UserType.STUDENT
            sess['email'] = userdata.email
            sess.modified = True

    #verify student is logged in and can see the assignment
    rv = client.get('/assignments', follow_redirects=True)
    assert rv.status_code == 200
    html_content = rv.get_data(as_text=True) #big string
    assert "Logged in as " in html_content
    assert "student: " in html_content
    assert "JohnDoe" in html_content
    assert "Algebra II" in html_content
    assert "Solve for x:   3x + 4 = 13" in html_content 	#assignment description
    assert "5" in html_content					#assignment worth
    assert "0.00" in html_content				#course grade (0.00 because nothing graded)
    assert "Submit Assignment" in html_content			#this verifies the POST method is available for submission

    #post data for student to submit to an assignment
    ## SUBMIT TO ASSIGNMENT ##
    #since there exists the possibility of multiple courses that each can have multiple assignments, 
    #the data for assignment_id is actually inside of the html
    #we'll just retrieve the id manually by querying the database
    with client.application.app_context():
        #algebra = Course.query.filter_by(name="Algebra II").first()
        #courseIdToPass = algebra.id
        assignment = Assignment.query.filter_by(description="Solve for x:   3x + 4 = 13").first()
        assIdToPass = assignment.id

    #get path to static file
    test_path = os.path.join(SUBMISSION_DIR, "sampleSubmission.txt")
    with open(test_path, "rb") as submission:
        rv = client.post('/assignments', data = {
            "assignment_id" : assIdToPass,         #pass the assignment id so newSubmission inside of view function works properly
            "file_handle" : (submission, "sampleSubmission.txt")
        }, follow_redirects=True)

    #verify student has submitted with a flashed message
#    assert b"Congratulations, you've submitted an assignment. Check back after the instructor has graded it!" in rv.data
    html_content = rv.get_data(as_text=True)
    assert "Congratulations, you" in html_content
    assert "ve submitted an assignment. Check back after the instructor has graded it!" in html_content

    #switch back to Teacher to see if they can see the submission
    with client.application.app_context():
        if session_find_user_by_name("MathProfessor"):
            userdata, user = session_find_user_by_name("MathProfessor")
        else:
            print("Could not find user")

    print(f"DEBUG: {userdata.name}") #this is for testing purposes

    with client.application.test_request_context('/'):
        with client.session_transaction() as sess:

            sess['userobj'] = userdata.as_dict()
            sess['username'] = userdata.name
            sess['student'] = userdata.type == UserType.STUDENT
            sess['email'] = userdata.email
            sess.modified = True

    #go to Submissions page now
    rv = client.get("/submissions", follow_redirects=True)
    assert rv.status_code == 200
    html_content = rv.get_data(as_text=True) #big string
    assert "Logged in as " in html_content
    assert "teacher: " in html_content
    assert "MathProfessor" in html_content
    assert "Assignments You Published:" in html_content         #header for assignments/submissions
    assert "Solve for x:   3x + 4 = 13" in html_content         #assignment description
    assert "5" in html_content                                  #assignment worth
    assert "sampleSubmission.txt" in html_content               #submission file handle name
    assert "Post Submission Score" in html_content              #this verifies the POST method for submitting a grade

    #try to grade the assignment, let's say 4/5 so the student's course_grade shows up as 80.00%
    with client.application.app_context():
        submit = Submission.query.filter_by(file_handle="sampleSubmission.txt").first()
        submitId = submit.id
        course = Course.query.filter_by(name="Algebra II").first()
        courseId = course.id
        student = Student.query.filter_by(username="JohnDoe").first()
        studentId = student.id
    rv = client.post("/submissions", data = {
        "score":4,
        "submission_id":submitId,
        "student_id":studentId,
        "course_id":courseId
    }, follow_redirects=True)

    html_content = rv.get_data(as_text=True)
    assert "New score has been submitted." in html_content

    #FINALLY FINALLY, check to see that John's course grade for his first (and only) enrollment is 80 (4/5)
    with client.application.app_context():
        if session_find_user_by_name("JohnDoe"):
            userdata, user = session_find_user_by_name("JohnDoe")
        else:
            print("Could not find user")
        enrollment_iter = user.enrollments
        test_enroll = enrollment_iter[0]
        assert test_enroll.course_grade == 80
