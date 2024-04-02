from rest_framework import serializers
from app.models import QuestionAnswer


class QuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswer
        fields = ["id", "user_course_enrollment", "question", "answer"]
        extra_kwargs = {'id': {'read_only': True}}
