from app.models import GptReview


class GptReviewAccessor:

    @classmethod
    def get_gpt_review_by_id(cls, id) -> GptReview | None:
        return GptReview.objects.filter(id=id).first()

    @classmethod
    def get_gpt_review_by_answer(cls, answer_id) -> GptReview | None:
        return GptReview.objects.filter(user_answer_id=answer_id).first()
