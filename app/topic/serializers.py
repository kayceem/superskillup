from rest_framework import serializers
from app.models import Topic


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'url', 'course']
        extra_kwargs = {'id': {'read_only': True}}
