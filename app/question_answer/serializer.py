from django.forms import ValidationError
from rest_framework import serializers
from app.models import QuestionAnswer


class QuestionAnswerSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        question = attrs.get('question')
        user_course_enrollment = attrs.get('user_course_enrollment')
        print(question.course)
        print(user_course_enrollment.course)
        if question.course != user_course_enrollment.course:
            raise ValidationError("Question course must match with user's enrolled course.")
        return super().validate(attrs)

    class Meta:
        model = QuestionAnswer
        fields = ["id", "user_course_enrollment", "question", "answer", "is_reviewed_by_gpt", "is_reviewed_by_manager",]
        extra_kwargs = {'id': {'read_only': True}}
