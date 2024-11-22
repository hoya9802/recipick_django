"""
Serializers for freemarket APIs.
"""
from rest_framework import serializers

from recipe.serializers import (
    NicknameSerializer,
    RecipeImageSerializer
)

from freemarket.models import Freemarket


class FreemarketListSerializer(serializers.ModelSerializer):
    """자유시장 List view을 위한 serializer"""
    user = NicknameSerializer(read_only=True)

    class Meta:
        model = Freemarket
        fields = [
            'id',
            'user',
            'name',
            'image',
            'is_shared',
        ]
        read_only_fields = ['id']


class FreemarketSerializer(FreemarketListSerializer):
    class Meta(FreemarketListSerializer.Meta):
        fields = FreemarketListSerializer.Meta.fields + [
            'count',
            'purchase_dt',
            'description',
        ]


class FreemarketImageSerializer(RecipeImageSerializer):
    """자유시장 이미지 업로드를 위한 Serializer"""
    class Meta(RecipeImageSerializer.Meta):
        model = Freemarket
        fields = RecipeImageSerializer.Meta.fields
