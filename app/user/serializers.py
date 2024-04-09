from rest_framework import serializers
from app.models import UserProfile
from app.utils.hashing import hash_raw_password
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'email', 'password', 'profile_image']
        extra_kwargs = {'id': {'read_only': True}, 'password': {'write_only': True}}

    def validate_password(self, value):
        validate_password(value)
        return value


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
