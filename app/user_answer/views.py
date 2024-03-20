from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import AdminAuthentication, UserAuthentication
from app.user_answer.user_answer import UserAnswer
from app.api.response_builder import ResponseBuilder
from app.user.user import User
from app.user_answer.serializer import UserAnswerSerializer
from app.api import api

@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_answer_by_user_id(request):
    response_builder = ResponseBuilder()
    user = request.user
    data = UserAnswer.get_answer_by_user(user.id)
    if data:
        serializer = UserAnswerSerializer(data, many = True)
        return response_builder.get_200_success_response("Data Fetched", serializer.data)
    return response_builder.get_404_not_found_response(api.USER_ANSWER_NOT_FOUND)

@api_view(["POST"])
@authentication_classes([UserAuthentication])
def add_answer(request):
    response_builder = ResponseBuilder()
    data = request.data
    data["user"] = request.user.id
    question = data["question"]
    answer_obj = UserAnswer.get_answer_by_question(question)
    if answer_obj:
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "Answer already submitted")
    serializer = UserAnswerSerializer(data = data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_200_success_response("Answer successfully added", serializer.data)

@api_view(["PUT", "PATCH"])
@authentication_classes([UserAuthentication])
def update_answer(request, id):
    response_builder = ResponseBuilder()
    user = request.user
    answer_obj = UserAnswer.get_answer_by_id(id)
    if answer_obj:
        if answer_obj.user == user:
            serializer = UserAnswerSerializer(answer_obj,data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return response_builder.get_200_success_response("Answer updated", serializer.data)
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "Access denied")
    return response_builder.get_404_not_found_response(api.USER_ANSWER_NOT_FOUND)

@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_answer_by_id(request, id):
    response_builder = ResponseBuilder()
    data = UserAnswer.get_answer_by_id(id)
    if data:
        serializer = UserAnswerSerializer(data)
        return response_builder.get_200_success_response("Data fetched", serializer.data)
    return response_builder.get_404_not_found_response(api.USER_ANSWER_NOT_FOUND)





