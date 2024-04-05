from rest_framework.decorators import api_view, authentication_classes, parser_classes
from app.shared.authentication import UserAuthentication
from app.user_assignment_submission.user_assignment_submission import UserAssignmentSubmission
from app.api.response_builder import ResponseBuilder
from app.user_assignment_submission.serializer import UserAssignmentSubmissionSerializer
from app.api import api
from rest_framework.parsers import MultiPartParser


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_user_assignment_submission_by_id(request, id):
    response_builder = ResponseBuilder()
    assignment_submission = UserAssignmentSubmission.get_user_assignment_submission_by_id(id)
    if not assignment_submission:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_SUBMISSION_NOT_FOUND)
    user = UserAssignmentSubmission.get_user_assignment_submission_user(assignment_submission)
    if user != request.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    serializer = UserAssignmentSubmissionSerializer(assignment_submission)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_user_assignment_submission_by_user_assignment(request, user_assignment_id):
    response_builder = ResponseBuilder()
    assignment_submission = UserAssignmentSubmission.get_user_assignment_submission_by_user_assignment(user_assignment_id)
    if not assignment_submission:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_SUBMISSION_NOT_FOUND)
    user = UserAssignmentSubmission.get_user_assignment_submission_user(assignment_submission)
    if user != request.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    serializer = UserAssignmentSubmissionSerializer(assignment_submission)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["POST"])
@authentication_classes([UserAuthentication])
@parser_classes([MultiPartParser])
def add_assignment_submission(request):
    user = request.user
    response_builder = ResponseBuilder()
    serializer = UserAssignmentSubmissionSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    if user != serializer.validated_data['user_assignment'].user_course_enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    serializer.save()
    return response_builder.get_201_success_response("Assignment successfully added", serializer.data)


@api_view(["PUT", "PATCH"])
@authentication_classes([UserAuthentication])
@parser_classes([MultiPartParser])
def update_assignment_submission(request, id):
    user = request.user
    is_PATCH = request.method == 'PATCH'
    response_builder = ResponseBuilder()
    assignment_submission = UserAssignmentSubmission.get_user_assignment_submission_by_id(id)
    if not assignment_submission:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_SUBMISSION_NOT_FOUND)
    user = UserAssignmentSubmission.get_user_assignment_submission_user(assignment_submission)
    if user != request.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    serializer = UserAssignmentSubmissionSerializer(assignment_submission, data=request.data, partial=is_PATCH)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("Assignment successfully updated", serializer.data)
