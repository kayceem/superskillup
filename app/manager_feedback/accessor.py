from app.models import ManagerFeedback


class ManagerFeedbackAccessor:

    @staticmethod
    def get_feedback_by_id(id):
        return ManagerFeedback.objects.filter(id=id).first()

    @staticmethod
    def get_all_feedback():
        return ManagerFeedback.objects.all()

    @staticmethod
    def get_feedback_by_gpt_review(gpt_review_id):
        return ManagerFeedback.objects.filter(gpt_review=gpt_review_id).first()
