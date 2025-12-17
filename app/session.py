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
    course_names, course_ids, user_type, id, user_from_query = __query_user_data(find_by_name, name, is_student)
    session['userobj'] = UserData(
        type=user_type, 
        name=name, 
        id=id, 
        email=email, 
        course_names=course_names,
        course_ids=course_ids
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
    return session_find_user(find_by_name, name)

'''find_by = find_by_name|find_by_id '''
def session_find_user(find_by, value: str|int) -> tuple[UserData|bool, Student|Teacher|None]:
    # NOTE:(khanh): only get the course name since the actual 
    # Course class cannot be passed into html via dict

    user = find_by(Student, value)
    course_names, course_ids, user_type, user_id, user_from_query = __query_user_data(find_by, value, bool(user), user)
    result = UserData(
        type=user_type, 
        name=name, 
        id=user_from_query.id if user_from_query else 0,
        email=user_from_query.email if user_from_query else "",
        course_names=associated_course_names,
        course_ids=associated_course_ids
    )
    return result, user_from_query

'''find_by = find_by_name|find_by_id '''
def __query_user_data(
    find_by, 
    value: str|int,
    is_student: bool, 
    user_from_query: Student|Teacher|None = 0
) -> tuple[ 
    # really sick of python's dynamic typing 
    "associated_course_names: List[str]",
    "associated_course_ids: List[int]",
    "user_type: UserType",
    "user_id: int", 
    "user_from_query: Student|Teacher"
]:
    associated_course_names: List[str]
    associated_course_ids: List[int]
    user_id: user_id
    user_type: UserType
    if not user_from_query:
        if is_student:
            return __query_student_data(find_by, value)
        else:
            return __query_teacher_data(find_by, value)

    user_id = user_from_query.id
    if is_student:
        user_type = UserType.STUDENT
        associated_course_names, associated_course_ids = __get_course_data_from_student(user_from_query)
    else:
        user_type = UserType.TEACHER
        associated_course_names, associated_course_ids = __get_course_data_from_teacher(user_from_query)

    return associated_course_names, associated_course_ids, user_type, user_id, user_from_query

def __query_student_data(
    find_fn,
    value: str|int,
) -> tuple[ 
    "associated_course_names: List[str]",
    "associated_course_ids: List[int]",
    "user_type: UserType",
    "user_id: int", 
    "user_from_query: Student"
]:
    student = find_fn(Student, value)
    if not student:
        return [], [], UserType.NOT_LOGGED_IN, 0, None

    associated_course_names, associated_course_ids = __get_course_data_from_student(student)
    return associated_course_names, associated_course_ids, UserType.STUDENT, student.id, student

def __query_teacher_data(
    find_fn, 
    value: str|int
) -> tuple[
    "associated_course_names: str",
    "user_type: UserType",
    "user_id: int", 
    "user_from_query: Teacher"
]:
    teacher = find_fn(Teacher, value)
    if not teacher:
        return [], [], UserType.NOT_LOGGED_IN, 0, None

    associated_course_names, associated_course_ids = __get_course_data_from_teacher(teacher)
    return associated_course_names, associated_course_ids, UserType.TEACHER, teacher.id, teacher


def __get_course_data_from_student(
    student: Student
) -> tuple[
    List[str], 
    List[int]
]:
    course_names = []
    course_ids = []
    for enrollment in student.enrollments:
        # NOTE:(khanh): db query in loop? May be a perf concern, not a priority rn
        course = Course.query.filter_by(id=enrollment.course_id).first()
        course_names.append(course.name)
        course_ids.append(course.id)
    return course_names, course_id

def __get_course_data_from_teacher(
    teacher: Teacher
) -> tuple[
    List[str], 
    List[int]
]:
    course_iter = Course.query.filter_by(teacher_id=teacher.id)
    # NOTE:(khanh): perf is garbage, whatever
    course_names = [x.name for x in course_iter]
    course_ids = [x.id for x in course_iter]
    return course_names, course_ids

def find_by_id(typename: Student|Teacher, id: int) -> Student|Teacher:
    result = typename.query.filter_by(id=id).first()
    return result

def find_by_name(typename: Student|Teacher, name: str) -> Student|Teacher:
    result = typename.query.filter_by(name=name).first()
    return result

