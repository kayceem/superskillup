from rest_framework import serializers
from app.models import Course
from app.tag.serializer import TagSerializer


class CourseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags, many=True).data
        return representation

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'level', 'created_by', 'thumbnail', 'category', 'tags']
        extra_kwargs = {'id': {'read_only': True}}
