from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import AdminAuthentication
from app.shared.pagination import paginate
from app.question_answer.question_answer import QuestionAnswer
from app.api.response_builder import ResponseBuilder
from app.user.user import User
from app.question_answer.serializer import QuestionAnswerSerializer
from app.api import api
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment


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
def get_answers_by_enrollment(request, enrollment_id):
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(enrollment_id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    answers = QuestionAnswer.get_answers_by_enrollment(enrollment_id)
    if not answers:
        return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
    paginated_data, page_info = paginate(answers, request)
    serializer = QuestionAnswerSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_answer_by_id(request, id):
    response_builder = ResponseBuilder()
    answer = QuestionAnswer.get_answer_by_id(id)
    if not answer:
        return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
    serializer = QuestionAnswerSerializer(answer)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_answer_by_question(request, question_id, user_id):
    response_builder = ResponseBuilder()
    answer = QuestionAnswer.get_answer_by_question(user_id, question_id)
    if not answer:
        return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
    serializer = QuestionAnswerSerializer(answer)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)
