"""
Serializers for recipe APIs.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Recipe, Category, LikeNg, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


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
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta(RecipeListSerializer.Meta):
        model = Recipe
        fields = RecipeListSerializer.Meta.fields + [
            'time_minutes',
            'serving',
            'link',
            'description',
            'ingredients',
        ]

    def validate_category(self, value):
        if value and not Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("선택한 카테고리가 존재하지 않습니다.")
        return value

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
        category_name = validated_data.pop('category', None)
        recipe = Recipe.objects.create(**validated_data)

        if ingredients:
            ingredient_objects = Ingredient.objects.filter(
                name__in=[ingredient['name'] for ingredient in ingredients]
            )
            recipe.ingredients.set(ingredient_objects)

        if category_name:
            category = Category.objects.get(name=category_name)
            recipe.category = category
            recipe.save()
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        category_name = validated_data.pop('category', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if category_name:
            category = Category.objects.get(name=category_name)
            instance.category = category

        if ingredients is not None:
            ingredient_objects = Ingredient.objects.filter(
                name__in=[ingredient['name'] for ingredient in ingredients]
            )
            instance.ingredients.set(ingredient_objects)

        instance.save()
        return instance


class RecipeImageSerializer(serializers.ModelSerializer):
    """이미지 업로드를 위한 serializer"""

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}
