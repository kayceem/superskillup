from rest_framework import serializers
from app.models import Question
from app.question_answer.question_answer import QuestionAnswer


class QuestionSerilizer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["id", "question", "course", "topic", "sub_topic"]
        extra_kwargs = {'id': {'read_only': True}}


class UserQuestionSerilizer(QuestionSerilizer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["answered"] = QuestionAnswer.is_question_answered(self.context['user_id'], instance.id)
        return representation
