from flask import session
from .models import Teacher, Student, UserType, UserData, Enrollment


def session_update_current_user(user):
    session['userobj'] = user.as_dict()
    session['username'] = user.name
    session['student'] = user.type == UserType.STUDENT
    session['email'] = user.email

def session_remove_current_user():
    # remove user's data in the session, except for flashed messages
    for key in list(session.keys()):
        if not key.startswith('_'):
            session.pop(key, None)
    # dummy user with NOT_LOGGED_IN status
    # session_update_current_user(UserData())

def session_is_current_user_logged_in():
    user = session_get_current_user_dict()
    if not user: 
        return False
    return user['type'] != UserType.NOT_LOGGED_IN

def session_get_current_user_obj() -> UserData:
    user = session_get_current_user_dict()
    if not user: 
        return False

    result = UserData(user['type'], user['name'], user['email'], user['courses'])
    return result

def session_get_current_user_dict():
    if 'userobj' not in session:
        return False

    result = session['userobj']
    return result

'''Returns a falsey value if unsuccessful, otherwise returns UserData'''
def session_find_user_by_name(name) -> UserData|bool:
    user_type = UserType.STUDENT
    user = Student.query.filter_by(username=name).first()
    course_iter = {}
    courses = []
    if user:
        # student
        course_iter = Enrollment.query.filter_by(student_id=user.id)
    else:
        # teacher
        user_type = UserType.TEACHER
        user = Teacher.query.filter_by(username=name).first()
        if not user:
            return False
        course_iter = Course.query.filter_by(teacher_id=user.id)

    courses = [x for x in course_iter]
    result = UserData(type=user_type, name=user.username, email=user.email, courses=courses)
    return result

