from app.models import Question
from app.utils.utils import get_or_none

class QuestionAccessor:

    @staticmethod
    def get_question_by_question_id(id):
        return Question.objects.filter(id = id).first()

    @staticmethod
    def get_all_questions(course_id):
        return Question.objects.filter(course = course_id).all()
