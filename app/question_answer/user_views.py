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


@api_view(["POST"])
@authentication_classes([UserAuthentication])
def add_answer(request):
    response_builder = ResponseBuilder()
    serializer = QuestionAnswerSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    answer = QuestionAnswer.get_answer_by_id(serializer.data["id"])
    GptReview.add_gpt_review(answer)
    send_answer_submitted_mail(answer)
    return response_builder.get_200_success_response("Answer successfully added", serializer.data)


@api_view(["PUT", "PATCH"])
@authentication_classes([UserAuthentication])
def update_answer(request, id):
    response_builder = ResponseBuilder()
    user = request.user
    answer = QuestionAnswer.get_answer_by_id(id)
    if not answer:
        return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
    if user != answer.user_course_enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    serializer = QuestionAnswerSerializer(answer, data=request.data, partial=True)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    GptReview.update_gpt_review(answer)
    return response_builder.get_200_success_response("Answer successfully added", serializer.data)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_answer_by_id(request, id):
    response_builder = ResponseBuilder()
    user = request.user
    data = QuestionAnswer.get_answer_by_id(id)
    if data:
        if user == data.user_course_enrollment.user:
            serializer = QuestionAnswerSerializer(data)
            return response_builder.get_200_success_response("Data Fetched", serializer.data)
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_answers_by_assignment(request, assign_id):
    response_builder = ResponseBuilder()
    user = request.user
    assignment = UserCourseEnrollment.get_assignment_by_id(assign_id)
    if assignment:
        if assignment.user == user:
            data = QuestionAnswer.get_answers_by_assignment(assign_id)
            if data:
                paginated_data, page_info = paginate(data, request)
                serializer = QuestionAnswerSerializer(paginated_data, many=True)
                return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
            return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    return response_builder.get_404_not_found_response(api.USER_ENROLLED_COURSE_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_answers_by_user(request):
    response_builder = ResponseBuilder()
    user = request.user
    answer = QuestionAnswer.get_answers_by_user(user)
    if answer:
        paginated_data, page_info = paginate(answer, request)
        serializer = QuestionAnswerSerializer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
    return response_builder.get_404_not_found_response(api.QUESTION_ANSWER_NOT_FOUND)
