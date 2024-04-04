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
def get_all_assignments(request):
    user = request.user
    response_builder = ResponseBuilder()
    assignments = UserCourseEnrollment.get_assignments_of_user(user.id)
    if not assignments:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)
    paginated_data, page_info = paginate(assignments, request)
    serializer = UserCourseEnrollmentSerializer(paginated_data, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_assignment_by_id(request, id):
    user = request.user
    response_builder = ResponseBuilder()
    assignment = UserCourseEnrollment.get_assignment_by_id(id)
    if not assignment:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)
    if user != assignment.user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    serializer = UserCourseEnrollmentSerializer(assignment)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_assigned_courses(request):
    user = request.user
    response_builder = ResponseBuilder()
    courses = UserCourseEnrollment.get_user_assigned_courses(user.id)
    if not courses:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNED_COURSE_NOT_FOUND)
    serializer = CourseSerializer(courses, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_assigned_topics_by_course(request, id):
    user = request.user
    response_builder = ResponseBuilder()
    assigned_user, topics = UserCourseEnrollment.get_user_assigned_topics_by_course(assign_id)
    if not topics:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNED_TOPIC_NOT_FOUND)
    if user != assigned_user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    serializer = TopicSerializer(topics, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_assigned_sub_topics_by_topic(request, id, topic_id):
    user = request.user
    response_builder = ResponseBuilder()
    assigned_user, sub_topics = UserCourseEnrollment.get_user_assigned_sub_topics(id, topic_id)
    if not sub_topics:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNED_SUB_TOPIC_NOT_FOUND)
    if user != assigned_user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    serializer = SubTopicSerializer(sub_topics, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)


@api_view(["GET"])
@authentication_classes([UserAuthentication])
def get_assigned_questions(request, id):
    user = request.user
    response_builder = ResponseBuilder()
    assigned_user, questions = UserCourseEnrollment.get_user_assigned_questions(id)
    if not questions:
        return response_builder.get_404_not_found_response(api.USER_ASSIGNED_QUESTION_NOT_FOUND)
    if user != assigned_user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    serializer = QuestionSerilizer(questions, many=True)
    return response_builder.get_200_success_response("Data Fetched", serializer.data)
