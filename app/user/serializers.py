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

    def create(self, validated_data):
        validated_data['password'] = hash_raw_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
