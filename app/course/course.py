from app.course.accessor import CourseAccessor
from app.api import api


class Course:

    def __init__(self, course):
        self.course = course

    @staticmethod
    def get_course_by_id(course_id):
        return CourseAccessor.get_course_by_id(id=course_id)

    @staticmethod
    def get_all_courses():
        return CourseAccessor.get_all_courses()

    @staticmethod
    def get_courses_from_ids(course_ids):
        return CourseAccessor.get_courses_from_ids(course_ids)
