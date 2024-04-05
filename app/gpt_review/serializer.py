from rest_framework import serializers
from app.models import GptReview
from django.core.validators import MaxValueValidator, MinValueValidator


class GptReviewSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )

    class Meta:
        model = GptReview
        fields = ['id', 'question_answer', 'remarks', 'score']
        extra_kwargs = {'id': {'read_only': True}}
