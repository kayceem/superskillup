from rest_framework import serializers
from app.app_admin.serializers import AdminSerializer
from app.user.serializers import UserSerializer
from app.models import UserCourseEnrollment
from rest_framework.exceptions import ValidationError
from app.course.serializers import CourseSerializer
from app.topic.serializers import TopicSerializer
from app.sub_topic.serializers import SubTopicSerializer
from app.question.serializer import QuestionSerilizer


class UserCourseEnrollmentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['course'] = CourseSerializer(instance.course).data
        representation['enrolled_by'] = AdminSerializer(instance.enrolled_by).data
        return representation

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
