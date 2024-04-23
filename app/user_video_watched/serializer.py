from rest_framework import serializers
from app.models import UserVideoWatched
from app.sub_topic.sub_topic import SubTopic
from django.core.exceptions import ValidationError


class UserVideoWatchedSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        sub_topic = attrs.get('sub_topic')
        user_course_enrollment = attrs.get('user_course_enrollment')
        if sub_topic.topic.course != user_course_enrollment.course:
            raise ValidationError("Sub topic course and enrolled must be same")
        if not SubTopic.video_exists(sub_topic.id):
            raise ValidationError("Sub topic has no video.")
        return super().validate(attrs)

    class Meta:
        model = UserVideoWatched
        fields = ["user_course_enrollment", "sub_topic"]
