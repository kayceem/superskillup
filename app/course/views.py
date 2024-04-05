from rest_framework.decorators import api_view, authentication_classes, parser_classes
from app.api.response_builder import ResponseBuilder
from app.course.serializers import CourseSerializer
from app.api import api
from app.course.course import Course
from app.shared.authentication import AdminAuthentication
from app.shared.pagination import paginate
from rest_framework.parsers import MultiPartParser


@api_view(['GET'])
@authentication_classes([AdminAuthentication])
def get_all_courses(request):
    """
    Get all courses
    """
    response_builder = ResponseBuilder()
    courses = Course.get_all_courses()
    if not courses:
        return response_builder.get_404_not_found_response(api.COURSE_NOT_FOUND)
    paginated_courses, page_info = paginate(courses, request)
    serializer = CourseSerializer(paginated_courses, many=True)
    return response_builder.get_200_success_response("Courses found", serializer.data, page_info)


@api_view(['GET'])
@authentication_classes([AdminAuthentication])
def get_course_by_id(request, id):
    """
    Get the course by id
    """

    response_builder = ResponseBuilder()
    course = Course.get_course_by_id(course_id=id)
    if not course:
        return response_builder.get_404_not_found_response(api.COURSE_NOT_FOUND)
    serializer = CourseSerializer(course)
    return response_builder.get_200_success_response("Course found", serializer.data)


@api_view(['POST'])
@authentication_classes([AdminAuthentication])
@parser_classes([MultiPartParser])
def create_course(request):
    """
    Create a Course.
    """
    data = request.data.copy()
    data['created_by'] = request.user.id
    response_builder = ResponseBuilder()
    serializer = CourseSerializer(data=data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("Course created successfully", serializer.data)


@api_view(['PATCH', 'PUT'])
@authentication_classes([AdminAuthentication])
@parser_classes([MultiPartParser])
def update_course(request, id):
    """
    Update the provided course
    """
    response_builder = ResponseBuilder()
    is_PATCH = request.method == 'PATCH'
    course = Course.get_course_by_id(course_id=id)
    if not course:
        return response_builder.get_404_not_found_response(api.COURSE_NOT_FOUND)
    if course.created_by != request.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    serializer = CourseSerializer(course, data=request.data, partial=is_PATCH)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("Course updated successfully", serializer.data)


@api_view(['DELETE'])
@authentication_classes([AdminAuthentication])
def delete_course(request, id):
    """
    Delete course
    """
    response_builder = ResponseBuilder()
    course = Course.get_course_by_id(course_id=id)
    if not course:
        return response_builder.get_404_not_found_response(api.COURSE_NOT_FOUND)
    if course.created_by != request.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    deleted = Course.delete_course(course)
    if not deleted:
        return response_builder.get_200_fail_response(api.DELETE_ERROR)
    return response_builder.get_204_success_response()
