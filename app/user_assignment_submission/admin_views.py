from rest_framework.decorators import api_view, authentication_classes
from app.shared.authentication import AdminAuthentication
from app.user_assignment_submission.user_assignment_submission import UserAssignmentSubmission
from app.api.response_builder import ResponseBuilder
from app.user_assignment_submission.serializer import UserAssignmentSubmissionSerializer
from app.api import api


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_user_assignment_submission_by_id(request, id):
    response_builder = ResponseBuilder()
    user_assignment_submission = UserAssignmentSubmission.get_user_assignment_submission_by_id(id)
    if not user_assignment_submission:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_SUBMISSION_NOT_FOUND)
    serializer = UserAssignmentSubmissionSerializer(user_assignment_submission)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_user_assignment_submission_by_user_assignment(request, user_assignment_id):
    response_builder = ResponseBuilder()
    user_assignment_submission = UserAssignmentSubmission.get_user_assignment_submission_by_user_assignment(user_assignment_id)
    if not user_assignment_submission:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_SUBMISSION_NOT_FOUND)
    serializer = UserAssignmentSubmissionSerializer(user_assignment_submission)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)
