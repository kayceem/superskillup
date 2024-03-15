from rest_framework import serializers
from app.models import UserProfile
from app.utils.hashing import hash_raw_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()