from rest_framework import serializers
from app.models import GptReview


class GptReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = GptReview
        fields = ['id', 'user_answer', 'remarks', 'score']
        extra_kwargs = {'id': {'read_only': True}}
