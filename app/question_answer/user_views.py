from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import UserAuthentication
from app.shared.pagination import paginate
from app.question_answer.question_answer import QuestionAnswer
from app.api.response_builder import ResponseBuilder
from app.question_answer.serializer import QuestionAnswerSerializer
from app.api import api
from app.services.email_service import send_answer_submitted_mail
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from app.gpt_review.gpt_review import GptReview


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_answer_by_id(request, id):
    user = request.user
    response_builder = ResponseBuilder()
    answer = QuestionAnswer.get_answer_by_id(id)
    if not answer:
        return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
    if user != answer.user_course_enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    serializer = QuestionAnswerSerializer(answer)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_answer_by_question(request, question_id):
    user = request.user
    response_builder = ResponseBuilder()
    answer = QuestionAnswer.get_answer_by_question(user.id, question_id)
    if not answer:
        return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
    serializer = QuestionAnswerSerializer(answer)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["POST"])
@authentication_classes([UserAuthentication])
def add_answer(request):
    user = request.user
    response_builder = ResponseBuilder()
    serializer = QuestionAnswerSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    if user != serializer.validated_data['user_course_enrollment'].user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    serializer.save()
    answer = QuestionAnswer.get_answer_by_id(serializer.data["id"])
    GptReview.add_gpt_review(answer)
    # send_answer_submitted_mail(answer)
    return response_builder.get_201_success_response("Answer successfully added", serializer.data)


@api_view(["PUT", "PATCH"])
@authentication_classes([UserAuthentication])
def update_answer(request, id):
    user = request.user
    is_PATCH = request.method == 'PATCH'
    response_builder = ResponseBuilder()
    answer = QuestionAnswer.get_answer_by_id(id)
    if not answer:
        return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
    if user != answer.user_course_enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    serializer = QuestionAnswerSerializer(answer, data=request.data, partial=is_PATCH)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    GptReview.update_gpt_review(answer)
    return response_builder.get_201_success_response("Answer successfully added", serializer.data)
