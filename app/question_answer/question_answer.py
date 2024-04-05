from app.question_answer.accessor import QuestionAnswerAccessor
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment


class QuestionAnswer:

    @staticmethod
    def get_answer_by_id(id):
        return QuestionAnswerAccessor.get_answer_by_id(id)

    @staticmethod
    def get_answer_by_question(user_id, question_id):
        return QuestionAnswerAccessor.get_answer_by_question(user_id, question_id)
