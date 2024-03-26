from app.gpt_review.accessor import GptReviewAccessor
from app.gpt_review.serializer import GptReviewSerializer
from app.gpt_review.open_ai import OpenAI


class GptReview:

    def __init__(self, topic):
        self.topic = topic

    @staticmethod
    def get_gpt_review_by_id(id):
        return GptReviewAccessor.get_gpt_review_by_id(id=id)

    @staticmethod
    def get_gpt_review_by_answer(answer_id):
        return GptReviewAccessor.get_gpt_review_by_answer(answer_id)

    @staticmethod
    def add_gpt_review(answer):
        course = answer.user_course_assignment.course.name
        question = answer.question.question
        answer_text = answer.answer
        review = OpenAI.generate_review(course, question, answer_text)
        if not review:
            return None
        data = {'user_answer': answer.id, **review}
        serializer = GptReviewSerializer(data=data)
        if not serializer.is_valid():
            return None
        serializer.save()
        print(serializer.data)
        return serializer.data

    @classmethod
    def update_gpt_review(cls, answer):
        gpt_review = cls.get_gpt_review_by_answer(answer.id)
        course = answer.user_course_assignment.course.name
        question = answer.question.question
        answer_text = answer.answer
        review = OpenAI.generate_review(course, question, answer_text)
        if not review:
            return None
        data = {'user_answer': answer.id, **review}
        serializer = GptReviewSerializer(gpt_review, data=data, partial=True)
        if not serializer.is_valid():
            return None
        serializer.save()
        return serializer.data
