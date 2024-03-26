from app.ManagerFeedback.accessor import ManagerFeedbackAccessor
from app.gpt_review.gpt_review import GptReview


class ManagerFeedback:

    @staticmethod
    def get_feedback_by_id(id):
        return ManagerFeedbackAccessor.get_feedback_by_id(id)

    @staticmethod
    def get_all_feedback():
        return ManagerFeedbackAccessor.get_all_feedback()

    @staticmethod
    def get_feedback_by_answer(answer_id):
        gpt_review = GptReview.get_gpt_review_by_answer(answer_id)
        feedback = ManagerFeedbackAccessor.get_feedback_by_gpt_review(gpt_review)
        return feedback
