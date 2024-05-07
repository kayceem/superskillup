from rest_framework.decorators import api_view, authentication_classes, parser_classes
from app.user_assignment.user_assignment import UserAssignment
from app.shared.authentication import AdminAuthentication
from app.api.response_builder import ResponseBuilder
from app.user_assignment.serializer import AdminUserAssignmentSerializer
from app.shared.pagination import paginate
from app.api import api
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(tags=['admin-user-assignment'], method='get', responses={200: AdminUserAssignmentSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_all_user_assignments_by_user(request, user_id):
    """
    Get all user assignments of a user [multiple courses]
    """
    response_builder = ResponseBuilder()
    user_assignments = UserAssignment.get_all_user_assignments_by_user(user_id)
    if not user_assignments:
        return response_builder.get_200_fail_response(api.USER_ASSIGNMENT_NOT_FOUND, result=[])
    paginated_data, page_info = paginate(user_assignments, request)
    serializer = AdminUserAssignmentSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)


@swagger_auto_schema(tags=['admin-user-assignment'], method='get', responses={200: AdminUserAssignmentSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_all_user_assignments_by_course(request, course_id):
    """
    Get all user assignments of a course [multiple users]
    """
    response_builder = ResponseBuilder()
    user_assignments = UserAssignment.get_all_user_assignments_by_course(course_id)
    if not user_assignments:
        return response_builder.get_200_fail_response(api.USER_ASSIGNMENT_NOT_FOUND, result=[])
    paginated_data, page_info = paginate(user_assignments, request)
    serializer = AdminUserAssignmentSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)


@swagger_auto_schema(tags=['admin-user-assignment'], method='get', responses={200: AdminUserAssignmentSerializer})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_user_assignment_by_id(request, id):
    """
    Get user assignment by id
    """
    response_builder = ResponseBuilder()
    user_assignment = UserAssignment.get_user_assignment_by_id(id)
    if not user_assignment:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)
    serializer = AdminUserAssignmentSerializer(user_assignment)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@swagger_auto_schema(tags=['admin-user-assignment'], method='get', responses={200: AdminUserAssignmentSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_user_assignments_by_enrollment(request, enrollment_id):
    """
    Get user assignments by enrollment(user and course)
    """
    response_builder = ResponseBuilder()
    user_assignments = UserAssignment.get_user_assignments_by_enrollment(enrollment_id)
    if not user_assignments:
        return response_builder.get_200_fail_response(api.USER_ASSIGNMENT_NOT_FOUND, result=[])
    paginated_data, page_info = paginate(user_assignments, request)
    serializer = AdminUserAssignmentSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)


@swagger_auto_schema(tags=['admin-user-assignment'], method='get', responses={200: AdminUserAssignmentSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_user_assignments_by_course(request, user_id, course_id):
    """
    Get user assignments of user by course
    """
    response_builder = ResponseBuilder()
    user_assignments = UserAssignment.get_user_assignments_by_course(user_id, course_id)
    if not user_assignments:
        return response_builder.get_200_fail_response(api.USER_ASSIGNMENT_NOT_FOUND, result=[])
    paginated_data, page_info = paginate(user_assignments, request)
    serializer = AdminUserAssignmentSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)


@swagger_auto_schema(tags=['admin-user-assignment'], method='post', request_body=AdminUserAssignmentSerializer, responses={201: AdminUserAssignmentSerializer})
@api_view(['POST'])
@authentication_classes([AdminAuthentication])
def create_user_assignment(request):
    """
    Assign an assignment to user.
    """
    response_builder = ResponseBuilder()
    serializer = AdminUserAssignmentSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("User assigned successfully", serializer.data)


@swagger_auto_schema(tags=['admin-user-assignment'], methods=['patch', 'put'], request_body=AdminUserAssignmentSerializer, responses={201: AdminUserAssignmentSerializer})
@api_view(['PATCH', 'PUT'])
@authentication_classes([AdminAuthentication])
def update_user_assignment(request, id):
    """
    Update the provided users assignment
    """

    response_builder = ResponseBuilder()
    is_PATCH = request.method == 'PATCH'
    user_assignment = UserAssignment.get_user_assignment_by_id(id)
    if not user_assignment:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)
    serializer = AdminUserAssignmentSerializer(user_assignment, data=request.data, partial=is_PATCH)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("User assignment updated successfully", serializer.data)


@swagger_auto_schema(tags=['admin-user-assignment'], method='delete')
@api_view(["DELETE"])
@authentication_classes([AdminAuthentication])
def delete_user_assignment(request, id):
    response_builder = ResponseBuilder()
    user_assignment = UserAssignment.get_user_assignment_by_id(id)
    if not user_assignment:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)
    deleted = UserAssignment.delete_user_assignment(user_assignment)
    if not deleted:
        return response_builder.get_200_fail_response(api.DELETE_ERROR)
    return response_builder.get_204_success_response()
