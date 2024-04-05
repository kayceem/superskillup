from rest_framework import serializers
from app.models import Question


class QuestionSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["id", "question", "course", "topic", "sub_topic"]
        extra_kwargs = {'id': {'read_only': True}}
