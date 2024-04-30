from app.app_admin.app_admin import Admin
from app.course.course import Course
from app.question.question import Question
from app.question_answer.question_answer import QuestionAnswer
from app.sub_topic.sub_topic import SubTopic
from app.topic.topic import Topic
from app.user.user import User
from app.user_course_enrollment.accessor import UserCourseEnrollmentAcessor
from app.user_video_watched.user_video_watched import UserVideo


class UserCourseEnrollment:

    @staticmethod
    def get_all_enrollments():
        return UserCourseEnrollmentAcessor.get_all_enrollments()

    @staticmethod
    def get_enrollment_by_id(id):
        return UserCourseEnrollmentAcessor.get_enrollment_by_id(id)

    @staticmethod
    def get_course_completion(enrollment):
        total_questions = Question.get_total_questions(enrollment.course.id)
        answered_questions = QuestionAnswer.get_answered_questions_by_course(enrollment.user.id, enrollment.course.id)
        total_videos = SubTopic.get_total_videos(enrollment.course.id)
        watched_videos = UserVideo.get_watched_videos(enrollment.id)
        completed_percentage = UserCourseEnrollment.calculate_completion_percentage(total_questions, answered_questions, total_videos, watched_videos)
        return {
            'percentage': completed_percentage,
            'questions': {
                'total': total_questions,
                'answered': answered_questions
            },
            'videos': {
                'total': total_videos,
                'watched': watched_videos
            }
        }

    @staticmethod
    def calculate_completion_percentage(total_questions, answered_questions, total_videos, watched_videos):
        if total_questions == 0:
            question_percentage = 0
        else:
            question_percentage = (answered_questions / total_questions) * 100

        if total_videos == 0:
            video_percenatge = 0
        else:
            video_percenatge = (watched_videos / total_videos) * 100
        return (question_percentage + video_percenatge) / 2

    @staticmethod
    def get_course_completion_percentage(enrollment):
        total_questions = Question.get_total_questions(enrollment.course.id)
        answered_questions = QuestionAnswer.get_answered_questions_by_course(enrollment.user.id, enrollment.course.id)
        total_videos = SubTopic.get_total_videos(enrollment.course.id)
        watched_videos = UserVideo.get_watched_videos(enrollment.id)
        return UserCourseEnrollment.calculate_completion_percentage(total_questions, answered_questions, total_videos, watched_videos)

    @staticmethod
    def get_user_enrollments(user_id):
        return UserCourseEnrollmentAcessor.get_user_enrollments(user_id)

    @staticmethod
    def get_managers_of_user(user_id):
        managers = UserCourseEnrollmentAcessor.get_managers_of_user(user_id)
        if not managers:
            return None
        manager_ids = list(set([element['enrolled_by'] for element in managers]))
        return Admin.get_admins_from_ids(manager_ids)

    @staticmethod
    def get_enrolled_users(manager_id):
        users = UserCourseEnrollmentAcessor.get_users_of_manager(manager_id)
        if not users:
            return None
        user_ids = list(set([element['user'] for element in users]))
        return User.get_users_from_ids(user_ids)

    @staticmethod
    def delete_enrollment(enrollment):
        return enrollment.delete()

    @staticmethod
    def get_user_enrolled_courses(user_id):
        courses = UserCourseEnrollmentAcessor.get_user_enrolled_courses(user_id)
        if not courses:
            return None
        course_ids = [element['course'] for element in courses]
        return Course.get_courses_from_ids(course_ids)

    @staticmethod
    def get_topics_by_enrolled_course(course_id):
        return Topic.get_topics_by_course(course_id)

    @staticmethod
    def get_sub_topics_by_enrolled_topic(course_id, topic_id):
        return SubTopic.get_sub_topics_by_course_topic(course_id, topic_id)

    @staticmethod
    def get_questions_by_enrolled_sub_topic(course_id, sub_topic_id):
        return Question.get_questions_by_course_sub_topic(course_id, sub_topic_id)

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
        courses = cls.get_user_enrolled_courses(user.id)
        return cls.get_search_data(courses=courses, **kwargs)
