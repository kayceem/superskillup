from rest_framework.decorators import api_view, authentication_classes
from app.app_admin.serializers import AdminSerializer
from app.course.serializers import CourseSerializer
from app.question.serializer import QuestionSerilizer, UserQuestionSerilizer
from app.sub_topic.serializers import SubTopicSerializer, UserSubTopicSerializer
from app.topic.serializers import TopicSerializer, UserTopicSerializer
from app.topic.topic import Topic
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from app.shared.authentication import UserAuthentication
from app.api.response_builder import ResponseBuilder
from app.user_course_enrollment.serializer import UserCourseEnrollmentSerializer
from app.shared.pagination import paginate
from app.api import api
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(tags=['user-enrollment'], method='get', responses={200: UserCourseEnrollmentSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_all_enrollments(request):
    """
    Get all enrollments of user
    """
    user = request.user
    response_builder = ResponseBuilder()
    enrollments = UserCourseEnrollment.get_user_enrollments(user.id)
    if not enrollments:
        return response_builder.get_200_fail_response(api.USER_ENROLLMENT_NOT_FOUND, result=[])
    paginated_data, page_info = paginate(enrollments, request)
    serializer = UserCourseEnrollmentSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)


@swagger_auto_schema(tags=['user-enrollment'], method='get', responses={200: UserCourseEnrollmentSerializer})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_enrollment_by_id(request, id):
    """
    Get enrollment by id
    """
    user = request.user
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    if user != enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    serializer = UserCourseEnrollmentSerializer(enrollment)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@swagger_auto_schema(tags=['user-enrollment'], method='get', responses={200: CourseSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_enrolled_courses(request):
    """
    Get all enrolled courses
    """
    user = request.user
    response_builder = ResponseBuilder()
    courses = UserCourseEnrollment.get_user_enrolled_courses(user.id)
    if not courses:
        return response_builder.get_200_fail_response(api.USER_ENROLLED_COURSE_NOT_FOUND, result=[])
    serializer = CourseSerializer(courses, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@swagger_auto_schema(tags=['user-enrollment'], method='get', responses={200: AdminSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_managers_of_user(request):
    """
    Get managers of user
    """
    user = request.user
    response_builder = ResponseBuilder()
    managers = UserCourseEnrollment.get_managers_of_user(user.id)
    if not managers:
        return response_builder.get_200_fail_response(api.USER_ENROLLED_MANAGER_NOT_FOUND, result=[])
    serializer = AdminSerializer(managers, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@swagger_auto_schema(tags=['user-enrollment'], method='get', responses={200: UserTopicSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_enrolled_topics(request, id):
    """
    Get all topics of enrolled course by enrollment
    """
    user = request.user
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    if user != enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    topics = UserCourseEnrollment.get_topics_by_enrolled_course(enrollment.course.id)
    if not topics:
        return response_builder.get_200_fail_response(api.USER_ENROLLED_TOPIC_NOT_FOUND, result=[])
    serializer = UserTopicSerializer(topics, many=True, context={'enrollment': enrollment})
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@swagger_auto_schema(tags=['user-enrollment'], method='get', responses={200: UserSubTopicSerializer(many=True)})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_enrolled_sub_topics(request, id, topic_id):
    """
    Get all sub topics by enrollment and topic
    """
    user = request.user
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    if user != enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    topic = Topic.get_topic_by_id(topic_id)
    if not topic:
        return response_builder.get_400_bad_request_response(api.USER_ENROLLED_TOPIC_NOT_FOUND, "Topic locked")
    if UserCourseEnrollment.is_topic_locked(enrollment, topic):
        return response_builder.get_400_bad_request_response(api.USER_ENROLLED_SUB_TOPIC_NOT_FOUND, "Topic locked")
    sub_topics = UserCourseEnrollment.get_sub_topics_by_enrolled_topic(enrollment.course.id, topic_id)
    if not sub_topics:
        return response_builder.get_200_fail_response(api.USER_ENROLLED_SUB_TOPIC_NOT_FOUND, result=[])
    serializer = UserSubTopicSerializer(sub_topics, many=True, context={'enrollment_id': enrollment.id})
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@swagger_auto_schema(tags=['user-enrollment'], method='get', responses={200: QuestionSerilizer(many=True)})
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_enrolled_questions(request, id, sub_topic_id):
    """
    Get all questions by enrollment and sub-topic
    """
    user = request.user
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    if user != enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    questions = UserCourseEnrollment.get_questions_by_enrolled_sub_topic(enrollment.course.id, sub_topic_id)
    if not questions:
        return response_builder.get_200_fail_response(api.USER_ENROLLED_QUESTION_NOT_FOUND, result=[])
    serializer = UserQuestionSerilizer(questions, many=True, context={'user_id': user.id})
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@swagger_auto_schema(tags=['user-enrollment'], method='get')
@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_enrolled_course_completion(request, id):
    """
    Get course completion
    """
    user = request.user
    response_builder = ResponseBuilder()
    enrollment = UserCourseEnrollment.get_enrollment_by_id(id)
    if not enrollment:
        return response_builder.get_404_not_found_response(api.USER_ENROLLMENT_NOT_FOUND)
    if user != enrollment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    completion = UserCourseEnrollment.get_course_completion(enrollment)
    return response_builder.get_200_success_response("Data Fetched", completion)
