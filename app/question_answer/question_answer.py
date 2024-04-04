from app.question_answer.accessor import QuestionAnswerAccessor
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment


class QuestionAnswer:

    @staticmethod
    def get_all_answer():
        return QuestionAnswerAccessor.get_all_answer()

    @staticmethod
    def get_answer_by_id(id):
        return QuestionAnswerAccessor.get_answer_by_id(id)

    @staticmethod
    def get_answers_by_assignment(assign_id):
        return QuestionAnswerAccessor.get_answers_by_assignment(assign_id)

    @staticmethod
    def get_answers_by_user(user_id):
        assignments = UserCourseEnrollment.get_assignments_of_user(user_id)
        # answers = [QuestionAnswer.get_answers_by_assignment(assignment) for assignment in assignments]
        answers = [answer for assignment in assignments for answer in QuestionAnswer.get_answers_by_assignment(assignment)]
        return answers
