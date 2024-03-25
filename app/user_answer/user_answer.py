from app.user_answer.accessor import UserAnswerAccessor
from app.user_course_assignment.user_course_assignment import UserCourseAssignment


class UserAnswer:

    @staticmethod
    def get_all_answer():
        return UserAnswerAccessor.get_all_answer()

    @staticmethod
    def get_answer_by_id(id):
        return UserAnswerAccessor.get_answer_by_id(id)

    @staticmethod
    def get_answers_by_assignment(assign_id):
        return UserAnswerAccessor.get_answers_by_assignment(assign_id)

    @staticmethod
    def get_answers_by_user(user_id):
        assignments = UserCourseAssignment.get_assignments_of_user(user_id)
        # answers = [UserAnswer.get_answers_by_assignment(assignment) for assignment in assignments]
        answers = [answer for assignment in assignments for answer in UserAnswer.get_answers_by_assignment(assignment)]
        return answers
