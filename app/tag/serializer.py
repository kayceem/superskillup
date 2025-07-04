from rest_framework import serializers
from app.models import Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", "name"]
        extra_kwargs = {'id': {'read_only': True}}
