from rest_framework import serializers
from app.models import ManagerFeedback
from django.core.validators import MaxValueValidator, MinValueValidator


class ManagerFeedbackSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )

    class Meta:
        model = ManagerFeedback
        fields = ["id", "gpt_review", "remarks", "score"]
        extra_kwargs = {'id': {'read_only': True}}
