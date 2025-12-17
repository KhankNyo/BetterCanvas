from typing import List
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
    course_names, user_type, id, user_from_query = __query_user_data(name, is_student)
    session['userobj'] = UserData(
        type=user_type, 
        name=name, 
        id=id, 
        email=email, 
        course_names=course_names
    ).as_dict()


def session_remove_current_user():
    # remove user's data in the session, except for flashed messages
    for key in list(session.keys()):
        if not key.startswith('_'):
            session.pop(key, None)

def session_is_current_user_logged_in() -> bool:
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
    if 'userobj' not in session:
        # returns a default user (not logged in)
        return UserData().as_dict()

    result = session['userobj']
    return result


'''Returns a falsey value if unsuccessful, otherwise returns UserData'''
def session_find_user_by_name(name) -> tuple[UserData|bool, Student|Teacher|None]:
    # NOTE:(khanh): only get the course name since the actual 
    # Course class cannot be passed into html via dict
    course_names = []

    user = Student.query.filter_by(username=name).first()
    associated_course_names, user_type, user_id, user_from_query = __query_user_data(name, bool(user), user)
    result = UserData(
        type=user_type, 
        name=name, 
        id=user_from_query.id if user_from_query else 0,
        email=user_from_query.email if user_from_query else "",
        course_names=associated_course_names
    )
    return result, user_from_query

def __query_user_data(
    name: str, 
    is_student: bool, 
    user_from_query: Student|Teacher|None = 0
) -> tuple[ 
    # really sick of python's dynamic typing 
    "associated_course_names: str",
    "user_type: UserType",
    "user_id: int", 
    "user_from_query: Student|Teacher"
]:
    associated_course_names: List[str]
    user_id: user_id
    user_type: UserType
    if not user_from_query:
        if is_student:
            return __query_student_data(name)
        else:
            return __query_teacher_data(name)

    user_id = user_from_query.id
    if is_student:
        user_type = UserType.STUDENT
        associated_course_names = __get_course_names_from_student(user_from_query)
    else:
        user_type = UserType.TEACHER
        associated_course_names = __get_course_names_from_teacher(user_from_query)

    return associated_course_names, user_type, user_id, user_from_query

def __query_student_data(
    name: str
) -> tuple[ 
    "associated_course_names: str",
    "user_type: UserType",
    "user_id: int", 
    "user_from_query: Student"
]:
    student = Student.query.filter_by(username=name).first()
    if not student:
        return [], UserType.NOT_LOGGED_IN, 0, None

    associated_course_names = __get_course_names_from_student(student)
    return associated_course_names, UserType.STUDENT, student.id, student

def __query_teacher_data(
    name: str
) -> tuple[
    "associated_course_names: str",
    "user_type: UserType",
    "user_id: int", 
    "user_from_query: Teacher"
]:
    teacher = Teacher.query.filter_by(username=name).first()
    if not teacher:
        return [], UserType.NOT_LOGGED_IN, 0, None

    associated_course_names = __get_course_names_from_teacher(teacher)
    return associated_course_names, UserType.TEACHER, teacher.id, teacher


def __get_course_names_from_student(student: Student) -> List[str]:
    course_names = []
    for enrollment in student.enrollments:
        # NOTE:(khanh): db query in loop? May be a perf concern, not a priority rn
        course = Course.query.filter_by(id=enrollment.course_id).first()
        course_names.append(course.name)
    return course_names

def __get_course_names_from_teacher(teacher: Teacher) -> List[str]:
    course_iter = Course.query.filter_by(teacher_id=teacher.id)
    course_names = [x.name for x in course_iter]
    return course_names

