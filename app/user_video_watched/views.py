from rest_framework.decorators import api_view, authentication_classes
from app.api import api
from drf_yasg.utils import swagger_auto_schema
from app.api.response_builder import ResponseBuilder
from app.shared.authentication import UserAuthentication
from app.user_video_watched.serializer import UserVideoWatchedSerializer


@swagger_auto_schema(tags=['user-video'], method='post', responses={201: UserVideoWatchedSerializer})
@api_view(["POST"])
@authentication_classes([UserAuthentication])
def add_user_video(request):
    """
    Add video watched by user
    """
    user = request.user
    response_builder = ResponseBuilder()
    serializer = UserVideoWatchedSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    if user != serializer.validated_data['user_course_enrollment'].user:
        return response_builder.get_400_bad_request_response(api.UNAUTHORIZED, "User not authorized")
    serializer.save()
    return response_builder.get_201_success_response("Video added to watched", serializer.data)
