from rest_framework.decorators import api_view, authentication_classes, parser_classes
from app.api.response_builder import ResponseBuilder
from app.shared.pagination import paginate
from app.assignment.serializers import AssignmentSerializer
from app.api import api
from app.assignment.assignment import Assignment
from app.shared.authentication import AdminAuthentication
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(tags=['admin-assignment'], method='get', responses={200: AssignmentSerializer(many=True)})
@api_view(['GET'])
@authentication_classes([AdminAuthentication])
def get_assignments_by_course(request, course_id):
    """
    Get assignments of course
    """
    response_builder = ResponseBuilder()
    assignments = Assignment.get_assignments_by_course(course_id=course_id)
    if not assignments:
        return response_builder.get_404_not_found_response(api.ASSIGNMENT_NOT_FOUND)
    paginated_assignments, page_info = paginate(assignments, request)
    serializer = AssignmentSerializer(paginated_assignments, many=True)
    return response_builder.get_200_success_response("Assignments found", serializer.data, page_info)


@swagger_auto_schema(tags=['admin-assignment'], method='get', responses={200: AssignmentSerializer})
@api_view(['GET'])
@authentication_classes([AdminAuthentication])
def get_assignment_by_id(request, id):
    """
    Get the assignment by id
    """

    response_builder = ResponseBuilder()
    assignment = Assignment.get_assignment_by_id(id)
    if not assignment:
        return response_builder.get_404_not_found_response(api.ASSIGNMENT_NOT_FOUND)
    serializer = AssignmentSerializer(assignment)
    return response_builder.get_200_success_response("Assignment found", serializer.data)


@swagger_auto_schema(tags=['admin-assignment'], method='post', request_body=AssignmentSerializer, responses={201: AssignmentSerializer})
@api_view(['POST'])
@authentication_classes([AdminAuthentication])
@parser_classes([MultiPartParser])
def create_assignment(request):
    """
    Create an assignment.
    """
    data = request.data.copy()
    data['created_by'] = request.user.id
    response_builder = ResponseBuilder()
    serializer = AssignmentSerializer(data=data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("Assignment created successfully", serializer.data)


@swagger_auto_schema(tags=['admin-assignment'], methods=['patch', 'put'], request_body=AssignmentSerializer, responses={201: AssignmentSerializer})
@api_view(['PATCH', 'PUT'])
@authentication_classes([AdminAuthentication])
@parser_classes([MultiPartParser])
def update_assignment(request, id):
    """
    Update the provided assignment
    """

    response_builder = ResponseBuilder()
    is_PATCH = request.method == 'PATCH'
    assignment = Assignment.get_assignment_by_id(id)
    if not assignment:
        return response_builder.get_404_not_found_response(api.ASSIGNMENT_NOT_FOUND)
    serializer = AssignmentSerializer(assignment, data=request.data, partial=is_PATCH)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("Assignment updated successfully", serializer.data)


@swagger_auto_schema(tags=['admin-assignment'], method='delete')
@api_view(['DELETE'])
@authentication_classes([AdminAuthentication])
def delete_assignment(request, id):
    """
    Delete an assignment
    """
    response_builder = ResponseBuilder()
    assignment = Assignment.get_assignment_by_id(id)
    if not assignment:
        return response_builder.get_404_not_found_response(api.ASSIGNMENT_NOT_FOUND)
    deleted = Assignment.delete_assignment(assignment)
    if not deleted:
        return response_builder.get_200_fail_response(api.DELETE_ERROR)
    return response_builder.get_204_success_response()
