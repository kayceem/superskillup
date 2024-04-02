from app.models import QuestionAnswer


class QuestionAnswerAccessor:

    @staticmethod
    def get_all_answer():
        return QuestionAnswer.objects.all()

    @staticmethod
    def get_answer_by_id(id):
        return QuestionAnswer.objects.filter(id=id).first()

    @staticmethod
    def get_answers_by_assignment(assign_id):
        return QuestionAnswer.objects.filter(user_course_enrollment=assign_id).all()
