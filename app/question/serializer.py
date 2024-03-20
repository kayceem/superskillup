from rest_framework import serializers
from app.models import Question

class QuestionSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["id", "question", "helping_text", "level", "course", "topic", "sub_topic", "url"]
        