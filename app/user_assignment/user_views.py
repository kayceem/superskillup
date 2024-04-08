from rest_framework.decorators import api_view, authentication_classes
from app.user_assignment.user_assignment import UserAssignment
from app.shared.authentication import UserAuthentication
from app.api.response_builder import ResponseBuilder
from app.user_assignment.serializer import UserAssignmentSerializer
from app.shared.pagination import paginate
from app.api import api
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(tags=['user-assignment'], method='get', responses={200: UserAssignmentSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_all_user_assignments(request):
    """
    Get all assignments of a user [multiple courses]
    """
    user = request.user
    response_builder = ResponseBuilder()
    user_assignments = UserAssignment.get_all_user_assignments_by_user(user.id)
    if not user_assignments:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)
    paginated_data, page_info = paginate(user_assignments, request)
    serializer = UserAssignmentSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)


@swagger_auto_schema(tags=['user-assignment'], method='get', responses={200: UserAssignmentSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_user_assignments_by_course(request, course_id):
    user = request.user
    """
    Get all assignments of a user by course
    """
    response_builder = ResponseBuilder()
    user_assignments = UserAssignment.get_user_assignments_by_course(user.id, course_id)
    if not user_assignments:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)
    paginated_data, page_info = paginate(user_assignments, request)
    serializer = UserAssignmentSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)


@swagger_auto_schema(tags=['user-assignment'], method='get', responses={200: UserAssignmentSerializer})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_user_assignment_by_id(request, id):
    """
    Get assignment of a user by id
    """
    response_builder = ResponseBuilder()
    user_assignment = UserAssignment.get_user_assignment_by_id(id)
    if not user_assignment:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)
    user = UserAssignment.get_assignment_user(user_assignment)
    if user != request.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    serializer = UserAssignmentSerializer(user_assignment)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@swagger_auto_schema(tags=['user-assignment'], method='get', responses={200: UserAssignmentSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_user_assignments_by_enrollment(request, enrollment_id):
    """
    Get all assignments by enrollment (user and course)
    """
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(enrollment_id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    if enrollment.user != request.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User unauthorized")
    user_assignments = UserAssignment.get_user_assignments_by_enrollment(enrollment_id)
    if not user_assignments:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)
    paginated_data, page_info = paginate(user_assignments, request)
    serializer = UserAssignmentSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
