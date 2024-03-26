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

    @staticmethod
    def filter_courses(courses, type, query):
        if type != 'course' and type != 'global':
            return []
        filtered_courses = courses.filter(name__icontains=query).all()
        return filtered_courses

    @staticmethod
    def filter_topics(courses, type, query):
        if type != 'topic' and type != 'global':
            return []
        filtered_topics = [topic for course in courses for topic in course.topics.filter(name__icontains=query).all()]
        return filtered_topics

    @staticmethod
    def filter_sub_topics(courses, type, query):
        if type != 'sub_topic' and type != 'global':
            return []
        filtered_sub_topics = [sub_topic for course in courses for topic in course.topics.all() for sub_topic in topic.sub_topics.filter(name__icontains=query).all()]
        return filtered_sub_topics

    @staticmethod
    def filter_questions(courses, type, query):
        if type != 'question' and type != 'global':
            return []
        filtered_questions = [question for course in courses for question in course.course_questions.filter(question__icontains=query).all()]
        return filtered_questions

    @classmethod
    def get_search_data(cls, **kwargs):
        filtered_courses = cls.filter_courses(**kwargs)
        filtered_topics = cls.filter_topics(**kwargs)
        filtered_sub_topics = cls.filter_sub_topics(**kwargs)
        filtered_questions = cls.filter_questions(**kwargs)
        return {'courses': filtered_courses, 'topics': filtered_topics, 'sub_topics': filtered_sub_topics, 'questions': filtered_questions}

    @classmethod
    def get_search_results_admin(cls, **kwargs):
        courses = Course.get_all_courses()
        return cls.get_search_data(courses=courses, **kwargs)

    @classmethod
    def get_search_results_user(cls, user, **kwargs):
        courses = cls.get_user_assigned_courses(user.id)
        return cls.get_search_data(courses=courses, **kwargs)
