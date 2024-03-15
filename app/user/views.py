from rest_framework.decorators import api_view
from app.api.response_builder import ResponseBuilder
from app.user.serializers import ResendOTPSerializer, UserLoginSerializer, UserSerializer, OTPSerializer
from app.api import api
from app.utils import utils
from app.user.user import User
from django.utils import timezone
from app.services.email_service import send_otp_mail


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
    user = User.get_user_by_email(email=serializer.validated_data["email"])
    send_otp_mail(user)
    result = {
        "Message": "Please check you email."
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



@api_view(["POST"])
def check_otp(request):
    response_builder = ResponseBuilder()
    otp_serializer = OTPSerializer(data=request.data)
    if not otp_serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, otp_serializer.errors)
    user = User.get_user_by_email(otp_serializer.validated_data["email"])
    otp =otp_serializer.validated_data["otp"]
    if user.otp != otp:
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "Invalid OTP")
    otp_expired = User.check_otp_expired(user.email)
    if otp_expired:
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, "Invalid OTP")
    user.otp = None
    user.is_verified = True
    user.save()
    serializer = UserSerializer(user)
    result = {
        "user": serializer.data,
    }
    return response_builder.get_201_success_response("User successfully verified", result)


@api_view(["POST"])
def resend_otp(request):
    response_builder = ResponseBuilder()
    resend_serializer = ResendOTPSerializer(data = request.data)
    if not resend_serializer.is_valid():
        return response_builder.get_400_bad_request_response(api.INVALID_INPUT, resend_serializer.errors)
    user = User.get_user_by_email(resend_serializer.validated_data["email"])
    if user.is_verified:
        return response_builder.get_200_fail_response(api.USER_VERIFIED)
    otp_expired = User.check_otp_expired(user.email)
    if user.otp is None:
        send_otp_mail(user)
        result = {
            "Message": "Please check you email."
        }
        return response_builder.get_201_success_response("Email Sent.", result)
    else:
        if otp_expired:
            send_otp_mail(user)
            result = {
                "Message": "Please check you email."
            }
            return response_builder.get_201_success_response("Email sent.", result)
        return response_builder.get_200_fail_response(api.OTP_ALREADY_SENT)
    
