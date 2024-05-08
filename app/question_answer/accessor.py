from app.models import QuestionAnswer


class QuestionAnswerAccessor:

    @staticmethod
    def get_answer_by_id(id):
        return QuestionAnswer.objects.filter(id=id).first()

    @staticmethod
    def get_answer_by_question(user_id, question_id):
        return QuestionAnswer.objects.filter(question=question_id, user_course_enrollment__user=user_id).first()

    @staticmethod
    def get_answered_questions_by_course(user_id, course_id):
        return QuestionAnswer.objects.filter(user_course_enrollment__user=user_id, question__course=course_id).count()

    @staticmethod
    def is_question_answered(user_id, question_id):
        return QuestionAnswer.objects.filter(question=question_id, user_course_enrollment__user=user_id).exists()
