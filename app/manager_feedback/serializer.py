from rest_framework import serializers
from app.models import ManagerFeedback


class ManagerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerFeedback
        fields = ["id", "gpt_review", "remarks", "score"]
        extra_kwargs = {'id': {'read_only': True}}
