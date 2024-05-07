from rest_framework import serializers
from app.models import SubTopic
from app.user_video_watched.user_video_watched import UserVideo


class SubTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTopic
        fields = ['id', 'name', 'description', 'url', 'topic', 'video', 'video_length', 'file']
        extra_kwargs = {'id': {'read_only': True}}


class UserSubTopicSerializer(SubTopicSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['video_watched'] = UserVideo.is_video_watched(self.context['enrollment_id'], instance.id)
        return representation
