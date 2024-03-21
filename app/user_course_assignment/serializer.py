from rest_framework import serializers
from app.models import UserCourseAssignment


class UserCourseAssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCourseAssignment
        fields = ["id", "user", "course", "status", "assigned_by", "deadline"]
        extra_kwargs = {'id': {'read_only': True}}
