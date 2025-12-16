from werkzeug.security import generate_password_hash
from app.models import Student, Teacher, Course, UserType, UserData
from app.session import session_find_user_by_name, session_update_current_user
from app import g_DB as db
from flask import get_flashed_messages, session
import pytest

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
    assert "MathProfessor " in html_content

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
