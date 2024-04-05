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
    manager_feedback = ManagerFeedback.get_feedback_by_id(id)
    if not manager_feedback:
        return response_builder.get_404_not_found_response(api.MANAGER_FEEDBACK_NOT_FOUND)
    serializer = ManagerFeedbackSerializer(manager_feedback)
    if not is_user_admin(user):
        answered_user = ManagerFeedback.get_answered_user(manager_feedback)
        if answered_user != user:
            return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "Unauthorized")
        return response_builder.get_200_success_response("Data Fetched", serializer.data)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([CombinedAuthentication])
def get_feedback_by_answer(request, answer_id):
    response_builder = ResponseBuilder()
    user = request.user
    manager_feedback = ManagerFeedback.get_feedback_by_answer(answer_id)
    if not manager_feedback:
        return response_builder.get_404_not_found_response(api.MANAGER_FEEDBACK_NOT_FOUND)
    serializer = ManagerFeedbackSerializer(manager_feedback)
    if not is_user_admin(user):
        answered_user = ManagerFeedback.get_answered_user(manager_feedback)
        if answered_user != user:
            return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "Unauthorized")
        return response_builder.get_200_success_response("Data Fetched", serializer.data)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["POST"])
@authentication_classes([AdminAuthentication])
def add_manager_feedback(request):
    response_builder = ResponseBuilder()
    serializer = ManagerFeedbackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return response_builder.get_201_success_response("Feedback added", serializer.data)
    return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)


@api_view(["PUT", "PATCH"])
@authentication_classes([AdminAuthentication])
def update_manager_feedback(request, id):
    response_builder = ResponseBuilder()
    is_PATCH = request.method == 'PATCH'
    manager_feedback = ManagerFeedback.get_feedback_by_id(id)
    if not manager_feedback:
        return response_builder.get_404_not_found_response(api.MANAGER_FEEDBACK_NOT_FOUND)
    serializer = ManagerFeedbackSerializer(manager_feedback, data=request.data, partial=is_PATCH)
    if serializer.is_valid():
        serializer.save()
        return response_builder.get_201_success_response("Feedback added", serializer.data)
    return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
