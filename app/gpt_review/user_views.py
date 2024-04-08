from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import UserAuthentication, AdminAuthentication
from app.gpt_review.gpt_review import GptReview
from app.api.response_builder import ResponseBuilder
from app.gpt_review.serializer import GptReviewSerializer
from app.api import api
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(tags=['user-gpt-review'], method='get', responses={200: GptReviewSerializer})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_gpt_review_by_answer(request, answer_id):
    response_builder = ResponseBuilder()
    gpt_review = GptReview.get_gpt_review_by_answer(answer_id)
    if not gpt_review:
        return response_builder.get_404_not_found_response(api.GPT_REVIEW_NOT_FOUND)
    user = GptReview.get_user_of_gpt_review(gpt_review)
    if user != request.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    serializer = GptReviewSerializer(gpt_review)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)
