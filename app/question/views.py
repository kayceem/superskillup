from app.question.question import Question
from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import AdminAuthentication, UserAuthentication
from app.api.response_builder import ResponseBuilder
from app.question.serializer import QuestionSerilizer
from app.api import api
from app.shared.pagination import paginate

@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_all_questions(request, course_id):
    response_builder = ResponseBuilder()
    data = Question.get_all_questions(course_id)
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = QuestionSerilizer(paginated_data, many = True)
        return response_builder.get_200_success_response("Data fetched", serializer.data)
    return response_builder.get_200_fail_response(api.QUESTION_NOT_FOUND)

@api_view(["POST"])
@authentication_classes([AdminAuthentication])
def create_question(request):
    response_builder = ResponseBuilder()
    serializer = QuestionSerilizer(data = request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_200_success_response("Question successfully created", serializer.data)

@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_question_by_question_id(request, id):
    response_builder = ResponseBuilder()
    data = Question.get_question_by_question_id(id)
    if data:
        serializer = QuestionSerilizer(data)
        return response_builder.get_200_success_response("Data Fetched", serializer.data)
    return response_builder.get_200_fail_response(api.QUESTION_NOT_FOUND)

@api_view(["PUT", "PATCH"])
@authentication_classes([AdminAuthentication])
def update_question(request, question_id):
    response_builder = ResponseBuilder()
    ques_obj = Question.get_question_by_question_id(question_id)
    if ques_obj is None:
        return response_builder.get_404_not_found_response(api.QUESTION_NOT_FOUND)
    serializer = QuestionSerilizer(ques_obj,data = request.data, partial = True)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_200_success_response("Question successfully updated", serializer.data)