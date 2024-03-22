from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import AdminAuthentication, UserAuthentication
from app.user_answer.user_answer import UserAnswer
from app.api.response_builder import ResponseBuilder
from app.user.user import User
from app.user_answer.serializer import UserAnswerSerializer
from app.api import api


@api_view(["POST"])
@authentication_classes([UserAuthentication])
def add_answer(request):
    response_builder = ResponseBuilder()
    serializer = UserAnswerSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_200_success_response("Answer successfully added", serializer.data)


@api_view(["PUT", "PATCH"])
@authentication_classes([UserAuthentication])
def update_answer(request, id):
    response_builder = ResponseBuilder()
    user = request.user
    answer = UserAnswer.get_answer_by_id(id)
    if not answer:
        return response_builder.get_404_not_found_response(api.USER_ANSWER_NOT_FOUND)
    if user != answer.user_course_assignment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    serializer = UserAnswerSerializer(answer, data=request.data, partial=True)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_200_success_response("Answer successfully added", serializer.data)
