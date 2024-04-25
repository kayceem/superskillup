from rest_framework import serializers
from app.models import SubTopic


class SubTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTopic
        fields = ['id', 'name', 'description', 'url', 'topic', 'video', 'video_length', 'file']
        extra_kwargs = {'id': {'read_only': True}}
