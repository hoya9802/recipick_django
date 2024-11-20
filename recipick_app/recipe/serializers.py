"""
Serializers for recipe APIs.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Recipe, Category, LikeNg


class NicknameSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='level.name', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['nick_name', 'level']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class LikeNgSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeNg
        fields = ['id', 'rater', 'recipe_rated', 'rate']


class RecipeListSerializer(serializers.ModelSerializer):
    """Recipe List view을 위한 serializer"""
    user = NicknameSerializer(read_only=True)
    category = serializers.CharField(required=False)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'user',
            'category',
            'likes_count',
            'dislikes_count',
            'image'
        ]
        read_only_fields = ['id']

    def get_likes_count(self, obj):
        return LikeNg.objects.filter(recipe_rated=obj, rate=1).count()

    def get_dislikes_count(self, obj):
        return LikeNg.objects.filter(recipe_rated=obj, rate=-1).count()


class RecipeSerializer(RecipeListSerializer):
    """Serializer for recipes"""

    class Meta(RecipeListSerializer.Meta):
        model = Recipe
        fields = RecipeListSerializer.Meta.fields + [
            'time_minutes',
            'serving',
            'link',
            'description',
        ]

    def validate_category(self, value):
        if value and not Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("선택한 카테고리가 존재하지 않습니다.")
        return value

    def create(self, validated_data):
        category_name = validated_data.pop('category', None)
        recipe = Recipe.objects.create(**validated_data)
        if category_name:
            category = Category.objects.get(name=category_name)
            recipe.category = category
            recipe.save()
        return recipe

    def update(self, instance, validated_data):
        category_name = validated_data.pop('category', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if category_name:
            category = Category.objects.get(name=category_name)
            instance.category = category
        instance.save()
        return instance


class RecipeImageSerializer(serializers.ModelSerializer):
    """이미지 업로드를 위한 serializer"""

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': True}}
