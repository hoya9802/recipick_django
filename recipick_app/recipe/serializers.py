"""
Serializers for recipe APIs.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Recipe


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['nick_name']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'user','time_minutes', 'serving', 'description']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Recipe detail view을 위한 serializer"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['link']