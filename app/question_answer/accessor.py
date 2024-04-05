from app.models import QuestionAnswer


class QuestionAnswerAccessor:

    @staticmethod
    def get_answer_by_id(id):
        return QuestionAnswer.objects.filter(id=id).first()

    @staticmethod
    def get_answer_by_question(user_id, question_id):
        return QuestionAnswer.objects.filter(question=question_id, user_course_enrollment__user=user_id).first()
