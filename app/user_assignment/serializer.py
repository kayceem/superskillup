from rest_framework import serializers
from app.assignment.serializers import AssignmentSerializer
from app.models import UserAssignment
from django.core.exceptions import ValidationError
from app.user_assignment_submission.user_assignment_submission import UserAssignmentSubmission


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['submitted'] = True if UserAssignmentSubmission.get_user_assignment_submission_by_user_assignment(instance.id) else False
        return representation
