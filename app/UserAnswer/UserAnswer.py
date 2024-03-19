from app.UserAnswer.accessor import UserAnswerAccessor

class UserAnswer:
    
    @staticmethod
    def get_answer_by_user(user_id):
        return UserAnswerAccessor.get_answer_by_user(user_id)
    
    @staticmethod
    def get_answer_by_answer_id(id):
        return UserAnswerAccessor.get_answer_by_answer_id(id)