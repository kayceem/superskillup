from rest_framework import serializers
from app.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'url']
        extra_kwargs = {'password': {'read_only': True}}
