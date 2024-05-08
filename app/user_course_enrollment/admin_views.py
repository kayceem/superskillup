from rest_framework.decorators import api_view, authentication_classes
from app.course.serializers import CourseSerializer
from app.user.serializers import UserSerializer
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from app.shared.authentication import AdminAuthentication
from app.api.response_builder import ResponseBuilder
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from app.user_course_enrollment.serializer import UserCourseEnrollmentSerializer
from app.shared.pagination import paginate
from app.api import api
from app.user.user import User
from app.services import email_service
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(tags=['admin-user-enrollment'], method='get', responses={200: UserCourseEnrollmentSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_all_enrollments(request):
    """
    Get all enrollments [multiple users | multiple courses]
    """
    response_builder = ResponseBuilder()
    data = UserCourseEnrollment.get_all_enrollments()
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = UserCourseEnrollmentSerializer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
    return response_builder.get_200_fail_response(api.USER_ENROLLMENT_NOT_FOUND, result=[])


@swagger_auto_schema(tags=['admin-user-enrollment'], method='get', responses={200: UserCourseEnrollmentSerializer})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_enrollment_by_id(request, id):
    """
    Get enrollment by id
    """
    response_builder = ResponseBuilder()
    data = UserCourseEnrollment.get_enrollment_by_id(id)
    if data:
        serializer = UserCourseEnrollmentSerializer(data)
        return response_builder.get_200_success_response("Data Fetched", serializer.data)
    return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)


@swagger_auto_schema(tags=['admin-user-enrollment'], method='get', responses={200: UserCourseEnrollmentSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_user_enrollments(request, user_id):
    """
    Get all enrollments of user [multiple courses]
    """
    response_builder = ResponseBuilder()
    data = UserCourseEnrollment.get_user_enrollments(user_id)
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = UserCourseEnrollmentSerializer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
    return response_builder.get_200_fail_response(api.USER_ENROLLMENT_NOT_FOUND, result=[])


@swagger_auto_schema(tags=['admin-user-enrollment'], method='get', responses={200: UserSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_enrolled_users(request):
    """
    Get all enrolled users
    """
    user = request.user
    response_builder = ResponseBuilder()
    users = UserCourseEnrollment.get_enrolled_users(user.id)
    if not users:
        return response_builder.get_200_fail_response(api.USER_ENROLLMENT_NOT_FOUND, result=[])
    paginated_data, page_info = paginate(users, request)
    serializer = UserSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)


@swagger_auto_schema(tags=['admin-user-enrollment'], method='get', responses={200: CourseSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_user_enrolled_courses(request, user_id):
    """
    Get enrolled courses of a user
    """
    response_builder = ResponseBuilder()
    user = User.get_user_by_id(user_id)
    if not user:
        return response_builder.get_404_not_found_response(api.USER_NOT_FOUND)
    courses = UserCourseEnrollment.get_user_enrolled_courses(user_id)
    if not courses:
        return response_builder.get_200_fail_response(api.USER_ENROLLMENT_NOT_FOUND, result=[])
    serializer = CourseSerializer(courses, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@swagger_auto_schema(tags=['admin-user-enrollment'], method='post', request_body=UserCourseEnrollmentSerializer, responses={200: UserCourseEnrollmentSerializer})
@api_view(["POST"])
@authentication_classes([AdminAuthentication])
def create_user_course_enrollment(request):
    """
    Enroll user to a course
    """
    response_builder = ResponseBuilder()
    request.data["enrolled_by"] = request.user.id
    serializer = UserCourseEnrollmentSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    ernollment = UserCourseEnrollment.get_enrollment_by_id(serializer.data.get('id'))
    email_service.send_course_enrolled_mail(ernollment)
    return response_builder.get_201_success_response("User enrolled in course successfully", serializer.data)


@swagger_auto_schema(tags=['admin-user-enrollment'], methods=['put', 'patch'], request_body=UserCourseEnrollmentSerializer, responses={200: UserCourseEnrollmentSerializer})
@api_view(["PUT", "PATCH"])
@authentication_classes([AdminAuthentication])
def update_user_course_enrollment(request, id):
    is_PATCH = request.method == 'PATCH'
    """
    Update user course enrollment
    """
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    serializer = UserCourseEnrollmentSerializer(enrollment, request.data, partial=is_PATCH)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_201_success_response("Successfully updated", serializer.data)


@swagger_auto_schema(tags=['admin-user-enrollment'], method='delete')
@api_view(["DELETE"])
@authentication_classes([AdminAuthentication])
def delete_user_course_enrollment(request, id):
    """
    Delete user course enrollment
    """
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    deleted = UserCourseEnrollment.delete_enrollment(enrollment)
    if not deleted:
        return response_builder.get_200_fail_response(api.DELETE_ERROR)
    return response_builder.get_204_success_response()
