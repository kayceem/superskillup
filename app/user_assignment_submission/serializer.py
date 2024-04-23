from rest_framework import serializers
from app.models import UserAssignmentSubmission


class UserAssignmentSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAssignmentSubmission
        fields = ["id", "user_assignment", "file", "url", 'description']
        extra_kwargs = {'id': {'read_only': True}}
