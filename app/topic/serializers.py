from rest_framework import serializers
from app.models import Topic
from django.db.models import Sum
from app.user_course_enrollment.user_course_enrollment import UserCourseEnrollment
from app.sub_topic.sub_topic import SubTopic
from app.user_video_watched.user_video_watched import UserVideo


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'url', 'course']
        extra_kwargs = {'id': {'read_only': True}}


class UserTopicSerializer(TopicSerializer):
    def to_representation(self, instance):
        enrollment = self.context['enrollment']
        repesentation = super().to_representation(instance)
        repesentation['total'] = SubTopic.get_total_videos_topic(instance.id)
        repesentation['completed'] = UserVideo.get_watched_videos_topic(instance.id)
        repesentation['length'] = instance.sub_topics.aggregate(total_length=Sum('video_length'))['total_length'] or 0
        repesentation['locked'] = UserCourseEnrollment.is_topic_locked(enrollment, instance)
        return repesentation
