from app.question.accessor import QuestionAccessor

class Question:

    @staticmethod
    def get_all_questions(course_id):
        return QuestionAccessor.get_all_questions(course_id)
    
    @staticmethod
    def get_question_by_question_id(id):
        return QuestionAccessor.get_question_by_question_id(id)