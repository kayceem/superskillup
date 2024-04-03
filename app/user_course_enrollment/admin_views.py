from rest_framework.decorators import api_view, authentication_classes
from app.course.serializers import CourseSerializer
from app.question.serializer import QuestionSerilizer
from app.sub_topic.serializers import SubTopicSerializer
from app.topic.serializers import TopicSerializer
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from app.shared.authentication import AdminAuthentication, UserAuthentication
from app.api.response_builder import ResponseBuilder
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from app.user_course_enrollment.serializer import UserCourseEnrollmentSerializer
from app.shared.pagination import paginate
from app.api import api
from app.user.user import User
from app.services import email_service


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_all_assignments(request):
    response_builder = ResponseBuilder()
    data = UserCourseEnrollment.get_all_assignments()
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = UserCourseEnrollmentSerializer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
    return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_assignment_by_id(request, id):
    response_builder = ResponseBuilder()
    data = UserCourseEnrollment.get_assignment_by_id(id)
    if data:
        serializer = UserCourseEnrollmentSerializer(data)
        return response_builder.get_200_success_response("Data Fetched", serializer.data)
    return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_assignments_of_user(request, user_id):
    response_builder = ResponseBuilder()
    data = UserCourseEnrollment.get_assignments_of_user(user_id)
    if data:
        paginated_data, page_info = paginate(data, request)
        serializer = UserCourseEnrollmentSerializer(paginated_data, many=True)
        return response_builder.get_200_success_response("Data Fetched", serializer.data, page_info)
    return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_user_assigned_courses(request, user_id):
    response_builder = ResponseBuilder()
    user = User.get_user_by_id(user_id)
    if user:
        courses = UserCourseEnrollment.get_user_assigned_courses(user_id)
        if courses:
            course = CourseSerializer(courses, many=True)
            result = {"user": user.id, "data": course.data}
            return response_builder.get_200_success_response("Data Fetched", result)
        return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)
    return response_builder.get_404_not_found_response(api.USER_NOT_FOUND)


@api_view(["POST"])
@authentication_classes([AdminAuthentication])
def assign_course(request):
    response_builder = ResponseBuilder()
    data = request.data
    data["assigned_by"] = request.user.id
    serializer = UserCourseEnrollmentSerializer(data=data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    assignment = UserCourseEnrollment.get_assignment_by_id(serializer.data.get('id'))
    email_service.send_course_assigned_mail(assignment)
    return response_builder.get_200_success_response("Course Assigned Successfully", serializer.data)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_assigned_topics(request, assign_id):
    response_builder = ResponseBuilder()
    user, data = UserCourseEnrollment.get_user_assigned_topics_by_course(assign_id)
    if data is None:
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, user)
    serializer = TopicSerializer(data, many=True)
    result = {"user": user.email, "topics": serializer.data}
    return response_builder.get_200_success_response("Data Fetched", result)


@api_view(["PUT", "PATCH"])
@authentication_classes([AdminAuthentication])
def update_assigned_course(request, id):
    response_builder = ResponseBuilder()
    assign_obj = UserCourseEnrollment.get_assignment_by_id(id)
    if assign_obj:
        serializer = UserCourseEnrollmentSerializer(assign_obj, request.data, partial=True)
        if not serializer.is_valid():
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
        serializer.save()
        return response_builder.get_200_success_response("Successfully updated", serializer.data)
    return response_builder.get_404_not_found_response(api.USER_ASSIGNMENT_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_assigned_sub_topic(request, assign_id, topic_id):
    response_builder = ResponseBuilder()
    try:
        user, sub_topics = UserCourseEnrollment.get_user_assigned_sub_topics(assign_id, topic_id)
        if sub_topics is None:
            return response_builder.get_400_bad_request_response(api.INVALID_INPUT, user)
        serializer = SubTopicSerializer(sub_topics, many=True)
        result = {"user": user.email, "sub_topics": serializer.data}
        return response_builder.get_200_success_response("Data Fetched", result)
    except Exception as e:
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, str(e))


@api_view(["GET"])
@authentication_classes([AdminAuthentication])
def get_user_assigned_questions(request, assign_id):
    response_builder = ResponseBuilder()
    user, data = UserCourseEnrollment.get_user_assigned_questions(assign_id)
    if data is None:
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, user)
    serializer = QuestionSerilizer(data, many=True)
    result = {"user": user.email, "questions": serializer.data}
    return response_builder.get_200_success_response("Data Fetched", result)
