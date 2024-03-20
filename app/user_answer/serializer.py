from rest_framework import serializers
from app.models import UserAnswer

class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = ["id","user", "question", "answer"]
