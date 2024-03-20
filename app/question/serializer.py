from rest_framework import serializers
from app.models import Question


class QuestionSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["id", "question", "helping_text", "level", "course", "topic", "sub_topic", "url"]

    def validate(self, attrs):
        if attrs.get('sub_topic'):
            attrs['topic'] = attrs.get('sub_topic').topic
            attrs['course'] = attrs.get('topic').course
        if attrs.get('topic'):
            attrs['course'] = attrs.get('topic').course
        return super().validate(attrs)
