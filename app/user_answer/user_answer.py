from app.user_answer.accessor import UserAnswerAccessor

class UserAnswer:
    
    @staticmethod
    def get_answer_by_user(user_id):
        return UserAnswerAccessor.get_answer_by_user(user_id)
    
    @staticmethod
    def get_answer_by_id(id):
        return UserAnswerAccessor.get_answer_by_id(id)
    
    @staticmethod
    def get_answer_by_question(question):
        return UserAnswerAccessor.get_answer_by_question(question)