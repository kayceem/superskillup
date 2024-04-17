from rest_framework.decorators import api_view, authentication_classes, parser_classes
from app.api.response_builder import ResponseBuilder
from app.user.serializers import ResendOTPSerializer, UserLoginSerializer, UserSerializer, OTPSerializer
from app.api import api
from app.user.swagger import UserResponse
from app.utils import utils
from app.user.user import User
from django.utils import timezone
from app.services.email_service import send_otp_mail
from app.shared.authentication import AdminAuthentication
from app.shared.pagination import paginate
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(tags=['admin-user'], method='get', responses={200: UserSerializer(many=True)})
@api_view(['GET'])
@authentication_classes([AdminAuthentication])
def get_all_users(request):
    """
    Get all users
    """
    response_builder = ResponseBuilder()
    users = User.get_all_users()
    if not users:
        return response_builder.get_404_not_found_response(api.USER_NOT_FOUND)
    paginated_users, page_info = paginate(users, request)
    serializer = UserSerializer(paginated_users, many=True)
    return response_builder.get_200_success_response("Users found", serializer.data, page_info)


@swagger_auto_schema(tags=['user-auth'], method='post', request_body=UserSerializer, responses={201: UserResponse.response()})
@api_view(['POST'])
@parser_classes([MultiPartParser])
def register_user(request):
    """
    Register a User.
    """
    response_builder = ResponseBuilder()

    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, serializer.errors)
    serializer.save()
    user = User.get_user_by_email(email=serializer.validated_data["email"])
    send_otp_mail(user)
    result = {"message": "Please check you email."}

    return response_builder.get_201_success_response("User registered successfully", result)


@swagger_auto_schema(tags=['user-auth'], method='post', request_body=UserLoginSerializer, responses={200: UserResponse.response(message=False)})
@api_view(['POST'])
def login_user(request):
    """
    Login User and generate auth token.
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
    user = User.get_user_by_email(email=email)
    user_serializer = UserSerializer(user)
    result = {"access_token": auth_token, "user": user_serializer.data}
    return response_builder.get_200_success_response("User logged in successfully", result)


@swagger_auto_schema(tags=['user-auth'], method='post', request_body=OTPSerializer, responses={201: UserSerializer})
@api_view(["POST"])
def check_otp(request):
    """
    Verify otp
    """
    response_builder = ResponseBuilder()
    otp_serializer = OTPSerializer(data=request.data)
    if not otp_serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, otp_serializer.errors)
    user = User.get_user_by_email(otp_serializer.validated_data["email"])
    if not user:
        return response_builder.get_400_bad_request_response(api.USER_NOT_FOUND, "User is not registered")
    otp = otp_serializer.validated_data["otp"]
    if user.otp != otp:
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "Invalid OTP")
    otp_expired = User.check_otp_expired(user.email)
    if otp_expired:
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "Invalid OTP")
    user.otp = None
    user.is_verified = True
    user.save()
    return response_builder.get_201_success_response("User successfully verified")


@swagger_auto_schema(tags=['user-auth'], method='post', request_body=ResendOTPSerializer, responses={201: UserResponse.response()})
@api_view(["POST"])
def resend_otp(request):
    """
    Resend otp
    """
    response_builder = ResponseBuilder()
    resend_serializer = ResendOTPSerializer(data=request.data)
    if not resend_serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, resend_serializer.errors)
    user = User.get_user_by_email(resend_serializer.validated_data["email"])
    if not user:
        return response_builder.get_400_bad_request_response(api.USER_NOT_FOUND, "User is not registered")
    if user.is_verified:
        return response_builder.get_200_fail_response(api.USER_VERIFIED)
    otp_expired = User.check_otp_expired(user.email)
    if user.otp is None:
        send_otp_mail(user)
        result = {"message": "Please check you email."}
        return response_builder.get_201_success_response("Email Sent.", result)
    else:
        if otp_expired:
            send_otp_mail(user)
            result = {"message": "Please check you email."}
            return response_builder.get_201_success_response("Email sent.", result)
        return response_builder.get_200_fail_response(api.OTP_ALREADY_SENT)
