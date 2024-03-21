from app.course.course import Course
from app.topic.topic import Topic
from app.user_course_assignment.accessor import UserCourseAssignmentAcessor


class UserCourseAssignment:

    @staticmethod
    def get_all_assignments():
        return UserCourseAssignmentAcessor.get_all_assignments()

    @staticmethod
    def get_assignment_by_id(id):
        return UserCourseAssignmentAcessor.get_assignment_by_id(id)

    @staticmethod
    def get_assignments_of_user(user_id):
        return UserCourseAssignmentAcessor.get_assignments_of_user(user_id)

    @staticmethod
    def get_user_assigned_courses(user_id):
        courses = UserCourseAssignmentAcessor.get_user_assigned_courses(user_id)
        if not courses:
            return None
        course_ids = [element['course'] for element in courses]
        return Course.get_courses_from_ids(course_ids)

    @staticmethod
    def get_user_assigned_topics_by_course(assign_id):
        assignment = UserCourseAssignmentAcessor.get_assignment_by_id(assign_id)
        if not assignment:
            return "Assignment not found", None
        topics = assignment.course.topics.all()
        return assignment.user, topics

    @staticmethod
    def get_user_assigned_sub_topics(assign_id, topic_id):
        assignment = UserCourseAssignmentAcessor.get_assignment_by_id(assign_id)
        if not assignment:
            return "Assignment not found", None
        topics = assignment.course.topics.filter(id=topic_id).first()
        if not topics:
            return "Topics not Found", None
        sub_topics = assignment.course.topics.filter(id=topic_id).first().sub_topics.all()
        return assignment.user, sub_topics

    @staticmethod
    def get_user_assigned_questions(assign_id):
        assignment = UserCourseAssignmentAcessor.get_assignment_by_id(assign_id)
        if not assignment:
            return "Assignment not found", None
        questions = assignment.course.course_questions.all()
        return assignment.user, questions
