from rest_framework import serializers
from app.models import UserCourseEnrollment
from rest_framework.exceptions import ValidationError
from app.course.serializers import CourseSerializer
from app.topic.serializers import TopicSerializer
from app.sub_topic.serializers import SubTopicSerializer
from app.question.serializer import QuestionSerilizer


class UserCourseEnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCourseEnrollment
        fields = ["id", "user", "course", "status", "enrolled_by"]
        extra_kwargs = {'id': {'read_only': True}}


class SearchRequestSerializer(serializers.Serializer):
    type_choices = ['course', 'topic', 'sub_topic', 'question', 'global']
    type = serializers.CharField()
    query = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('type') and attrs.get('type') not in self.type_choices:
            raise ValidationError('Invalid type')
        return super().validate(attrs)


class SearchDataSerializer(serializers.Serializer):
    courses = CourseSerializer(many=True)
    topics = TopicSerializer(many=True)
    sub_topics = SubTopicSerializer(many=True)
    questions = QuestionSerilizer(many=True)
