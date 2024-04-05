from rest_framework.decorators import api_view
from app.app_admin.serializers import AdminLoginSerializer
from app.utils import utils
from app.api.response_builder import ResponseBuilder
from app.app_admin.app_admin import Admin
from app.api import api


@api_view(['POST'])
def login_admin(request):
    """
    Login admin and generate auth token.
    """

    response_builder = ResponseBuilder()
    serializer = AdminLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    status, auth_token = Admin.login(serializer.validated_data['username'], serializer.validated_data['password'])
    if utils.is_status_failed(status):
        return response_builder.get_200_fail_response(status)

    result = {
        "access_token": auth_token
    }
    return response_builder.get_200_success_response("Admin logged in successfully", result)
