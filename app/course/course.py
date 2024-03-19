from app.course.accessor import CourseAccessor
from app.api import api


class Course:

    def __init__(self, course):
        self.course = course

    @staticmethod
    def get_course_by_id(course_id):
        return CourseAccessor.get_course(id=course_id)

    @staticmethod
    def filter_course(query: dict):
        return CourseAccessor.filter_course(query)
