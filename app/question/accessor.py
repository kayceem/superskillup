from app.models import Question
from app.utils.utils import get_or_none


class QuestionAccessor:

    @staticmethod
    def get_question_by_id(id):
        return Question.objects.filter(id=id).first()

    @staticmethod
    def get_total_questions(course_id):
        return Question.objects.filter(course=course_id).count()

    @staticmethod
    def get_questions_by_course(course_id):
        return Question.objects.filter(course=course_id).all()

    @staticmethod
    def get_questions_by_sub_topic(sub_topic_id):
        return Question.objects.filter(sub_topic=sub_topic_id).all()

    @staticmethod
    def get_questions_by_course_sub_topic(course_id, sub_topic_id):
        return Question.objects.filter(course=course_id, sub_topic=sub_topic_id).all()
