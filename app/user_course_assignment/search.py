from rest_framework.decorators import api_view, authentication_classes
from app.user_course_assignment.user_course_assignment import UserCourseAssignment
from app.shared.authentication import CombinedAuthentication
from app.api.response_builder import ResponseBuilder
from app.user_course_assignment.user_course_assignment import UserCourseAssignment
from app.user_course_assignment.serializer import SearchRequestSerializer, SearchDataSerializer
from app.api import api
from app.utils import utils


@api_view(["GET"])
@authentication_classes([CombinedAuthentication])
def search(request):
    query_params = request.GET
    user = request.user
    is_admin = utils.is_user_admin(user)
    response_builder = ResponseBuilder()
    request_serializer = SearchRequestSerializer(data=query_params)
    if not request_serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_SEARCH_QUERY, request_serializer.errors)
    if is_admin:
        search_data = UserCourseAssignment.get_search_results_admin(**request_serializer.validated_data)
    else:
        search_data = UserCourseAssignment.get_search_results_user(user, **request_serializer.validated_data)
    data_serializer = SearchDataSerializer(search_data)
    return response_builder.get_200_success_response("Searched Data", data_serializer.data)
