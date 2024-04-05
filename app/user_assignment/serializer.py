from rest_framework import serializers
from app.assignment.serializers import AssignmentSerializer
from app.models import UserAssignment
from django.core.exceptions import ValidationError


class AdminUserAssignmentSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        assignment = attrs.get('assignment')
        user_course_enrollment = attrs.get('user_course_enrollment')
        if assignment.course != user_course_enrollment.course:
            raise ValidationError("Assignment course must match with user's enrolled course.")
        return super().validate(attrs)

    class Meta:
        model = UserAssignment
        fields = ["id", "user_course_enrollment", "assignment", "deadline"]
        extra_kwargs = {'id': {'read_only': True}}


class UserAssignmentSerializer(AdminUserAssignmentSerializer):
    assignment = AssignmentSerializer()
