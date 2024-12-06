"""
Serializers for help APIs.
"""
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from recipe.serializers import (
    NicknameSerializer,
    RecipeImageSerializer,
    IngredientSerializer
)

from recipe.models import Ingredient
from lab.models import Lab, Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'exlog']


class LabListSerializer(serializers.ModelSerializer):
    """지식인 List view을 위한 serializer"""
    user = NicknameSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, required=False)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Lab
        fields = [
            'id',
            'user',
            'title',
            'image',
            'ingredients',
            'modify_dt',
            'likes_count'
        ]
        read_only_fields = ['id']

    @extend_schema_field(serializers.IntegerField)
    def get_likes_count(self, obj):
        return Like.objects.filter(exlog=obj).count()

    def validate_ingredients(self, value):
        if value:
            ingredient_names = [ingredient['name'] for ingredient in value]
            existing_ingredients = Ingredient.objects.filter(
                name__in=ingredient_names
            ).values_list('name', flat=True)

            non_existing = set(ingredient_names) - set(existing_ingredients)
            if non_existing:
                raise serializers.ValidationError(
                    f"다음 재료들이 존재하지 않습니다: {', '.join(non_existing)}"
                )
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', [])
        print("Received ingredients:", ingredients)
        lab = Lab.objects.create(**validated_data)

        if ingredients:
            ingredient_objects = Ingredient.objects.filter(
                name__in=[ingredient['name'] for ingredient in ingredients]
            )
            lab.ingredients.set(ingredient_objects)

        return lab

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if ingredients is not None:
            ingredient_objects = Ingredient.objects.filter(
                name__in=[ingredient['name'] for ingredient in ingredients]
            )
            instance.ingredients.set(ingredient_objects)

        instance.save()
        return instance


class LabSerializer(LabListSerializer):

    class Meta(LabListSerializer.Meta):
        fields = LabListSerializer.Meta.fields + [
            'description'
        ]


class LabImageSerializer(RecipeImageSerializer):
    """지식인 이미지 업로드를 위한 Serializer"""
    class Meta(RecipeImageSerializer.Meta):
        model = Lab
        fields = RecipeImageSerializer.Meta.fields
