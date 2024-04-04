from rest_framework.decorators import api_view, authentication_classes
from app.course.serializers import CourseSerializer
from app.question.serializer import QuestionSerilizer
from app.sub_topic.serializers import SubTopicSerializer
from app.topic.serializers import TopicSerializer
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from app.shared.authentication import AdminAuthentication, UserAuthentication
from app.api.response_builder import ResponseBuilder
from app.user_course_enrollment.serializer import UserCourseEnrollmentSerializer
from app.shared.pagination import paginate
from app.api import api


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_all_enrollments(request):
    user = request.user
    response_builder = ResponseBuilder()
    enrollments = UserCourseEnrollment.get_user_enrollments(user.id)
    if not enrollments:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    paginated_data, page_info = paginate(enrollments, request)
    serializer = UserCourseEnrollmentSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_enrollment_by_id(request, id):
    user = request.user
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    if user != enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    serializer = UserCourseEnrollmentSerializer(enrollment)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_enrolled_courses(request):
    user = request.user
    response_builder = ResponseBuilder()
    courses = UserCourseEnrollment.get_user_enrolled_courses(user.id)
    if not courses:
        return response_builder.get_404_not_found_response(api.USER_ENROLLED_COURSE_NOT_FOUND)
    serializer = CourseSerializer(courses, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_enrolled_topics(request, id):
    user = request.user
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    if user != enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    topics = UserCourseEnrollment.get_topics_by_enrolled_course(enrollment.course.id)
    if not topics:
        return response_builder.get_404_not_found_response(api.USER_ENROLLED_TOPIC_NOT_FOUND)
    serializer = TopicSerializer(topics, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_enrolled_sub_topics(request, id, topic_id):
    user = request.user
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    if user != enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    sub_topics = UserCourseEnrollment.get_sub_topics_by_enrolled_topic(enrollment.course.id, topic_id)
    if not sub_topics:
        return response_builder.get_404_not_found_response(api.USER_ENROLLED_SUB_TOPIC_NOT_FOUND)
    serializer = SubTopicSerializer(sub_topics, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_enrolled_questions(request, id, sub_topic_id):
    user = request.user
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    if user != enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    questions = UserCourseEnrollment.get_questions_by_enrolled_sub_topic(enrollment.course.id, sub_topic_id)
    if not questions:
        return response_builder.get_404_not_found_response(api.USER_ENROLLED_QUESTION_NOT_FOUND)
    serializer = QuestionSerilizer(questions, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)
