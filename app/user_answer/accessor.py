from app.models import UserAnswer

class UserAnswerAccessor:

    @staticmethod
    def get_answer_by_user(user_id):
        return UserAnswer.objects.filter(user = user_id).all()
    
    @staticmethod
    def get_answer_by_id(id):
        return UserAnswer.objects.filter(id = id).first()
    
    @staticmethod
    def get_answer_by_question(question):
        return UserAnswer.objects.filter(question = question).first()