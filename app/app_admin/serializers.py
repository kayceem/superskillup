from rest_framework import serializers
from django.contrib.auth.models import User


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']
        extra_kwargs = {'id': {'read_only': True}, 'username': {'read_only': True}}


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
