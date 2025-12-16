from flask import session
from .models import Teacher, Student, UserType, UserData, Enrollment, Course


def session_update_current_user(userdata: UserData):
    session['userobj'] = userdata.as_dict()
    session['username'] = userdata.name
    session['student'] = userdata.type == UserType.STUDENT
    session['email'] = userdata.email

def session_add_current_user_locally(name, is_student, email):
    session['username'] = name
    session['student'] = is_student
    session['email'] = email

    user_type = UserType.TEACHER
    if is_student:
        user_type = UserType.STUDENT
    courses = __get_courses_associated_with_user(name, is_student, email)
    session['userobj'] = UserData(user_type, name, email, courses).as_dict()


def session_remove_current_user():
    # remove user's data in the session, except for flashed messages
    for key in list(session.keys()):
        if not key.startswith('_'):
            session.pop(key, None)

def session_current_user_is_logged_in() -> bool:
    user = session_get_current_user_obj()
    return user.type != UserType.NOT_LOGGED_IN

def session_get_current_user_obj() -> UserData:
    user = session_get_current_user_dict()
    result = UserData.from_dict(user)
    return result

'''Get the current user in session, 
    ALWAYS return a valid UserData class converted to dict
'''
def session_get_current_user_dict() -> dict:
    if 'username' not in session:
        # returns a default user (not logged in)
        return UserData().as_dict()

    result = session['userobj']
    return result

def __get_courses_associated_with_user(name, is_student) -> list:
    course_iter = { }
    if is_student:
        user = Student.query.filter_by(username=name).first()
        course_iter = Enrollment.query.filter_by(student_id=user.id)
    else:
        user = Teacher.query.filter_by(username=name).first()
        course_iter = Course.query.filter_by(teacher_id=user.id)
    courses = [x.name for x in course_iter]
    return courses

'''Returns a falsey value if unsuccessful, otherwise returns UserData'''
def session_find_user_by_name(name) -> tuple[UserData|bool, Student|Teacher|None]:
    user_type = UserType.STUDENT
    user = Student.query.filter_by(username=name).first()
    course_iter = {}
    # NOTE:(khanh): only get the course name since the actual 
    # Course class cannot be passed into html via dict
    course_names = []
    if user:
        # student
        for enrollment in user.enrollments:
            course = Course.query.filter_by(id=enrollment.course_id).first()
            course_names.append(course.name)
    else:
        # teacher
        user_type = UserType.TEACHER
        user = Teacher.query.filter_by(username=name).first()
        if not user:
            return False, user
        course_iter = Course.query.filter_by(teacher_id=user.id)
        course_names = [x.name for x in course_iter]
    result = UserData(usertype=user_type, name=user.username, email=user.email, course_names=course_names)
    return result, user

