"""
Serializers for help APIs.
"""
from rest_framework import serializers

from recipe.serializers import (
    NicknameSerializer,
    RecipeImageSerializer
)

from help.models import Help


class HelpListSerializer(serializers.ModelSerializer):
    """지식인 List view을 위한 serializer"""
    user = NicknameSerializer(read_only=True)

    class Meta:
        model = Help
        fields = [
            'id',
            'user',
            'title',
            'image',
            'modify_dt',
        ]
        read_only_fields = ['id']


class HelpSerializer(HelpListSerializer):
    class Meta(HelpListSerializer.Meta):
        fields = HelpListSerializer.Meta.fields + [
            'description'
        ]


class HelpImageSerializer(RecipeImageSerializer):
    """지식인 이미지 업로드를 위한 Serializer"""
    class Meta(RecipeImageSerializer.Meta):
        model = Help
        fields = RecipeImageSerializer.Meta.fields
