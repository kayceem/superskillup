from app.manager_feedback.manager_feedback import ManagerFeedback
from rest_framework.decorators import api_view, authentication_classes
from app.api.response_builder import ResponseBuilder
from app.api import api
from app.shared.authentication import AdminAuthentication, CombinedAuthentication
from app.manager_feedback.serializer import ManagerFeedbackSerializer
from app.shared.pagination import paginate
from app.user.user import User
from app.utils.utils import is_user_admin


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_all_feedback(request):
    response_builder = ResponseBuilder()
    data = ManagerFeedback.get_all_feedback()
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = ManagerFeedbackSerializer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
    return response_builder.get_404_not_found_response(api.MANAGER_FEEDBACK_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([CombinedAuthentication])
def get_feedback_by_id(request, id):
    response_builder = ResponseBuilder()
    user = request.user
    data = ManagerFeedback.get_feedback_by_id(id)
    serializer = ManagerFeedbackSerializer(data)
    if data:
        if not is_user_admin(user):
            answered_user = data.gpt_review.user_answer.user_course_assignment.user
            if answered_user == user:
                return response_builder.get_200_success_response("Data Fetched", serializer.data)
            return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "Access Denied")
        else:
            return response_builder.get_200_success_response("Data Fetched", serializer.data)
    else:
        return response_builder.get_404_not_found_response(api.MANAGER_FEEDBACK_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([CombinedAuthentication])
def get_feedback_by_answer(request, answer_id):
    response_builder = ResponseBuilder()
    user = request.user
    data = ManagerFeedback.get_feedback_by_answer(answer_id)
    serializer = ManagerFeedbackSerializer(data)
    if data:
        if not is_user_admin(user):
            answered_user = data.gpt_review.user_answer.user_course_assignment.user
            if answered_user == user:
                return response_builder.get_200_success_response("Data Fetched", serializer.data)
            return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "Access Denied")
        else:
            return response_builder.get_200_success_response("Data Fetched", serializer.data)
    else:
        return response_builder.get_404_not_found_response(api.MANAGER_FEEDBACK_NOT_FOUND)


@api_view(["POST"])
@authentication_classes([AdminAuthentication])
def add_manager_feedback(request):
    response_builder = ResponseBuilder()
    serializer = ManagerFeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return response_builder.get_200_success_response("Feedback added", serializer.data)
    return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)


@api_view(["PUT", "PATCH"])
@authentication_classes([AdminAuthentication])
def update_manager_feedback(request, id):
    response_builder = ResponseBuilder()
    feedback_obj = ManagerFeedback.get_feedback_by_id(id)
    if not feedback_obj:
        return response_builder.get_404_not_found_response(api.MANAGER_FEEDBACK_NOT_FOUND)
    serializer = ManagerFeedbackSerializer(feedback_obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return response_builder.get_200_success_response("Feedback added", serializer.data)
    return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
