from rest_framework.decorators import api_view, authentication_classes
from app.api.response_builder import ResponseBuilder
from app.course.serializers import CourseSerializer
from app.api import api
from app.course.course import Course
from app.shared.authentication import AdminAuthentication


@api_view(['POST'])
@authentication_classes([AdminAuthentication])
def create_course(request):
    """
    Create a Course.
    """

    response_builder = ResponseBuilder()
    serializer = CourseSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("Course created successfully", serializer.data)


@api_view(['PATCH', 'PUT'])
@authentication_classes([AdminAuthentication])
def update_course(request, id):
    """
    Update the provided course
    """

    response_builder = ResponseBuilder()
    is_PATCH = request.method == 'PATCH'
    course = Course.get_course_by_id(course_id=id)
    if not course:
        return response_builder.get_404_not_found_response(api.COURSE_NOT_FOUND)
    serializer = CourseSerializer(course, data=request.data, partial=is_PATCH)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("Course updated successfully", serializer.data)


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


@api_view(['GET'])
@authentication_classes([AdminAuthentication])
def get_all_courses(request):
    """
    Get the course by id
    """
    response_builder = ResponseBuilder()
    courses = Course.filter_course({})
    if not courses:
        return response_builder.get_404_not_found_response(api.COURSE_NOT_FOUND)
    serializer = CourseSerializer(courses, many=True)
    return response_builder.get_200_success_response("Courses found", serializer.data)
