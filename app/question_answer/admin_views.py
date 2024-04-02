from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import AdminAuthentication
from app.shared.pagination import paginate
from app.question_answer.question_answer import QuestionAnswer
from app.api.response_builder import ResponseBuilder
from app.user.user import User
from app.question_answer.serializer import QuestionAnswerSerializer
from app.api import api


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_answers_by_user(request, user_id):
    response_builder = ResponseBuilder()
    user = User.get_user_by_id(user_id)
    if user:
        answer = QuestionAnswer.get_answers_by_user(user_id)
        if answer:
            paginated_data, page_info = paginate(answer, request)
            serializer = QuestionAnswerSerializer(paginated_data, many=True)
            return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
        return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
    return response_builder.get_404_not_found_response(api.USER_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_all_answer(request):
    response_builder = ResponseBuilder()
    data = QuestionAnswer.get_all_answer()
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = QuestionAnswerSerializer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
    return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_answer_by_id(request, id):
    response_builder = ResponseBuilder()
    data = QuestionAnswer.get_answer_by_id(id)
    if data:
        serializer = QuestionAnswerSerializer(data)
        return response_builder.get_200_success_response("Data Fetched", serializer.data)
    return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_answers_by_assignment(request, assign_id):
    response_builder = ResponseBuilder()
    data = QuestionAnswer.get_answers_by_assignment(assign_id)
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = QuestionAnswerSerializer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
    return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
