from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import AdminAuthentication
from app.shared.pagination import paginate
from app.question_answer.question_answer import QuestionAnswer
from app.api.response_builder import ResponseBuilder
from app.question_answer.serializer import QuestionAnswerSerializer
from app.api import api
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(tags=['admin-answer'], method='get', responses={200: QuestionAnswerSerializer})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_answer_by_id(request, id):
    """
        Get answer by id
    """
    response_builder = ResponseBuilder()
    answer = QuestionAnswer.get_answer_by_id(id)
    if not answer:
        return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
    serializer = QuestionAnswerSerializer(answer)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@swagger_auto_schema(tags=['admin-answer'], method='get', responses={200: QuestionAnswerSerializer})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_answer_by_question(request, question_id, user_id):
    """
        Get answer(of a user) by question
    """
    response_builder = ResponseBuilder()
    answer = QuestionAnswer.get_answer_by_question(user_id, question_id)
    if not answer:
        return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
    serializer = QuestionAnswerSerializer(answer)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)
