from rest_framework import serializers
from app.models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'course', 'description', 'url', 'created_by', 'file',]
        extra_kwargs = {'id': {'read_only': True}}
