from rest_framework import serializers
from app.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'level', 'created_by', 'thumbnail', 'category', 'tags']
        extra_kwargs = {'id': {'read_only': True}}
