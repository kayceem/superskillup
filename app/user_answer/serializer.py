from rest_framework import serializers
from app.models import UserAnswer


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = ["id", "user_course_assignment", "question", "answer"]
        extra_kwargs = {'id': {'read_only': True}}
