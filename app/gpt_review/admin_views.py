from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import UserAuthentication, AdminAuthentication
from app.gpt_review.gpt_review import GptReview
from app.api.response_builder import ResponseBuilder
from app.gpt_review.serializer import GptReviewSerializer
from app.api import api


# @api_view(["GET"])
# @authentication_classes([AdminAuthentication])
# def get_gpt_review_by_id(request, id):
#     response_builder = ResponseBuilder()
#     gpt_review = GptReview.get_gpt_review_by_id(id)
#     if not gpt_review:
#         return response_builder.get_404_not_found_response(api.GPT_REVIEW_NOT_FOUND)
#     serializer = GptReviewSerializer(gpt_review)
#     return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_gpt_review_by_answer(request, answer_id):
    response_builder = ResponseBuilder()
    gpt_review = GptReview.get_gpt_review_by_answer(answer_id)
    if not gpt_review:
        return response_builder.get_404_not_found_response(api.GPT_REVIEW_NOT_FOUND)
    serializer = GptReviewSerializer(gpt_review)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)
