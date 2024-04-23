from app.question_answer.accessor import QuestionAnswerAccessor


class QuestionAnswer:

    @staticmethod
    def get_answer_by_id(id):
        return QuestionAnswerAccessor.get_answer_by_id(id)

    @staticmethod
    def get_answer_by_question(user_id, question_id):
        return QuestionAnswerAccessor.get_answer_by_question(user_id, question_id)

    @staticmethod
    def get_answered_questions_by_course(user_id, course_id):
        return QuestionAnswerAccessor.get_answered_questions_by_course(user_id, course_id)
