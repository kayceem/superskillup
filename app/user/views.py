from rest_framework.decorators import api_view
from app.api.response_builder import ResponseBuilder
from app.user.serializers import UserLoginSerializer, UserSerializer
from app.api import api
from app.utils import utils
from app.user.user import User


@api_view(['POST'])
def register_user(request):
    """
    Register a borrower.
    """
    response_builder = ResponseBuilder()

    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    result = {
        "borrower": serializer.data,
        "access_token": User(serializer.instance).generate_auth_token()
    }

    return response_builder.get_201_success_response("User registered successfully", result)


@api_view(['POST'])
def login_user(request):
    """
    Login borrower and generate auth token.
    """

    response_builder = ResponseBuilder()

    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)

    email = serializer.validated_data["email"]
    password = serializer.validated_data["password"]

    status, auth_token = User.login(email, password)
    if utils.is_status_failed(status):
        return response_builder.get_200_fail_response(status)

    result = {
        "access_token": auth_token
    }

    return response_builder.get_200_success_response("User logged in successfully", result)

