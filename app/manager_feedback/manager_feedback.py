from app.manager_feedback.accessor import ManagerFeedbackAccessor
from app.gpt_review.gpt_review import GptReview


class ManagerFeedback:

    @staticmethod
    def get_feedback_by_id(id):
        return ManagerFeedbackAccessor.get_feedback_by_id(id)

    @staticmethod
    def get_all_feedback():
        return ManagerFeedbackAccessor.get_all_feedback()

    @staticmethod
    def get_answered_user(manager_feedback):
        if not manager_feedback:
            return None
        return manager_feedback.gpt_review.question_answer.user_course_enrollment.user

    @staticmethod
    def get_feedback_by_answer(answer_id):
        gpt_review = GptReview.get_gpt_review_by_answer(answer_id)
        if not gpt_review:
            return None
        return ManagerFeedbackAccessor.get_feedback_by_gpt_review(gpt_review)
