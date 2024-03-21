from rest_framework import serializers
from app.models import UserAnswer


class UserCourseAssignment(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = ["id", "user", "course", "status", "assigned_by", "deadline"]
        extra_kwargs = {'id': {'read_only': True}}
