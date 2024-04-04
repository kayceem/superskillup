from app.question.question import Question
from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import AdminAuthentication, UserAuthentication
from app.api.response_builder import ResponseBuilder
from app.question.serializer import QuestionSerilizer
from app.api import api
from app.shared.pagination import paginate


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_questions_by_course(request, course_id):
    response_builder = ResponseBuilder()
    data = Question.get_questions_by_course(course_id)
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = QuestionSerilizer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data fetched", serializer.data, page_info)
    return response_builder.get_200_fail_response(api.QUESTION_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_questions_by_sub_topic(request, sub_topic_id):
    response_builder = ResponseBuilder()
    data = Question.get_questions_by_sub_topic(sub_topic_id)
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = QuestionSerilizer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data fetched", serializer.data, page_info)
    return response_builder.get_200_fail_response(api.QUESTION_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_question_by_id(request, id):
    response_builder = ResponseBuilder()
    data = Question.get_question_by_id(id)
    if data:
        serializer = QuestionSerilizer(data)
        return response_builder.get_200_success_response("Data Fetched", serializer.data)
    return response_builder.get_200_fail_response(api.QUESTION_NOT_FOUND)


@api_view(["POST"])
@authentication_classes([AdminAuthentication])
def create_question(request):
    response_builder = ResponseBuilder()
    serializer = QuestionSerilizer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_200_success_response("Question successfully created", serializer.data)


@api_view(["PUT", "PATCH"])
@authentication_classes([AdminAuthentication])
def update_question(request, id):
    is_PATCH = request.method == 'PATCH'
    response_builder = ResponseBuilder()
    question = Question.get_question_by_id(id)
    if question is None:
        return response_builder.get_404_not_found_response(api.QUESTION_NOT_FOUND)
    serializer = QuestionSerilizer(question, data=request.data, partial=is_PATCH)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_200_success_response("Question successfully updated", serializer.data)


@api_view(["DELETE"])
@authentication_classes([AdminAuthentication])
def delete_question(request, id):
    response_builder = ResponseBuilder()
    question = Question.get_question_by_id(id)
    if question is None:
        return response_builder.get_404_not_found_response(api.QUESTION_NOT_FOUND)
    deleted = Question.delete_question(question)
    if not deleted:
        return response_builder.get_200_fail_response(api.DELETE_ERROR)
    return response_builder.get_204_success_response()
