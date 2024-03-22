from app.models import UserAnswer


class UserAnswerAccessor:

    @staticmethod
    def get_all_answer():
        return UserAnswer.objects.all()

    @staticmethod
    def get_answer_by_id(id):
        return UserAnswer.objects.filter(id=id).first()

    @staticmethod
    def get_answers_by_assignment(assign_id):
        return UserAnswer.objects.filter(user_course_assignment=assign_id).all()
