from rest_framework.decorators import api_view, authentication_classes
from app.course.serializers import CourseSerializer
# from app.question.serializer import QuestionSerilizer
# from app.sub_topic.serializers import SubTopicSerializer
# from app.topic.serializers import TopicSerializer
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from app.shared.authentication import AdminAuthentication
from app.api.response_builder import ResponseBuilder
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from app.user_course_enrollment.serializer import UserCourseEnrollmentSerializer
from app.shared.pagination import paginate
from app.api import api
from app.user.user import User
from app.services import email_service


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_all_enrollments(request):
    response_builder = ResponseBuilder()
    data = UserCourseEnrollment.get_all_enrollments()
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = UserCourseEnrollmentSerializer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
    return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_enrollment_by_id(request, id):
    response_builder = ResponseBuilder()
    data = UserCourseEnrollment.get_enrollment_by_id(id)
    if data:
        serializer = UserCourseEnrollmentSerializer(data)
        return response_builder.get_200_success_response("Data Fetched", serializer.data)
    return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_user_enrollments(request, user_id):
    response_builder = ResponseBuilder()
    data = UserCourseEnrollment.get_user_enrollments(user_id)
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = UserCourseEnrollmentSerializer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
    return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_user_enrolled_courses(request, user_id):
    response_builder = ResponseBuilder()
    user = User.get_user_by_id(user_id)
    if not user:
        return response_builder.get_404_not_found_response(api.USER_NOT_FOUND)
    courses = UserCourseEnrollment.get_user_enrolled_courses(user_id)
    if not courses:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    serializer = CourseSerializer(courses, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["POST"])
@authentication_classes([AdminAuthentication])
def create_user_course_enrollment(request):
    response_builder = ResponseBuilder()
    request.data["enrolled_by"] = request.user.id
    serializer = UserCourseEnrollmentSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    ernollment = UserCourseEnrollment.get_enrollment_by_id(serializer.data.get('id'))
    email_service.send_course_enrolled_mail(ernollment)
    return response_builder.get_200_success_response("User enrolled in course successfully", serializer.data)


@api_view(["PUT", "PATCH"])
@authentication_classes([AdminAuthentication])
def update_user_course_enrollment(request, id):
    is_PATCH = request.method == 'PATCH'
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    serializer = UserCourseEnrollmentSerializer(enrollment, request.data, partial=is_PATCH)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    return response_builder.get_200_success_response("Successfully updated", serializer.data)


@api_view(["DELETE"])
@authentication_classes([AdminAuthentication])
def delete_user_course_enrollment(request, id):
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    deleted = UserCourseEnrollment.delete_enrollment(enrollment)
    if not deleted:
        return response_builder.get_200_fail_response(api.DELETE_ERROR)
    return response_builder.get_204_success_response()


# @api_view(["GET"])
# @authentication_classes([AdminAuthentication])
# def get_assigned_topics(request, id):
#     response_builder = ResponseBuilder()
#     user, data = UserCourseEnrollment.get_user_assigned_topics_by_course(id)
#     if data is None:
#         return response_builder.get_400_bad_request_response(api.INVALID_INPUT, user)
#     serializer = TopicSerializer(data, many=True)
#     result = {"user": user.email, "topics": serializer.data}
#     return response_builder.get_200_success_response("Data Fetched", result)


# @api_view(["GET"])
# @authentication_classes([AdminAuthentication])
# def get_assigned_sub_topic(request, id, topic_id):
#     response_builder = ResponseBuilder()
#     try:
#         user, sub_topics = UserCourseEnrollment.get_user_assigned_sub_topics(id, topic_id)
#         if sub_topics is None:
#             return response_builder.get_400_bad_request_response(api.INVALID_INPUT, user)
#         serializer = SubTopicSerializer(sub_topics, many=True)
#         result = {"user": user.email, "sub_topics": serializer.data}
#         return response_builder.get_200_success_response("Data Fetched", result)
#     except Exception as e:
#         return response_builder.get_400_bad_request_response(api.INVALID_INPUT, str(e))


# @api_view(["GET"])
# @authentication_classes([AdminAuthentication])
# def get_user_assigned_questions(request, id):
#     response_builder = ResponseBuilder()
#     user, data = UserCourseEnrollment.get_user_assigned_questions(id)
#     if data is None:
#         return response_builder.get_400_bad_request_response(api.INVALID_INPUT, user)
#     serializer = QuestionSerilizer(data, many=True)
#     result = {"user": user.email, "questions": serializer.data}
#     return response_builder.get_200_success_response("Data Fetched", result)
