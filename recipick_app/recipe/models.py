import uuid
import os

from django.conf import settings
from django.db import models


def recipe_image_file_path(instance, filename):
    """새로운 이미지에대한 이미지 경로 생성"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads', 'recipe', filename)


class Category(models.Model):
    name = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe 객체"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    name = models.CharField(max_length=255)
    time_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    serving = models.PositiveSmallIntegerField()
    link = models.URLField(null=True, blank=True)
    description = models.TextField()
    create_dt = models.DateField(auto_now_add=True)
    modify_dt = models.DateField(auto_now=True)
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.name


class LikeNg(models.Model):
    """LikeNg 객체"""
    rater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    recipe_rated = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    rate = models.SmallIntegerField(choices=[(-1, 'Dislike'), (1, 'Like')])
    create_dt = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.recipe_rated} - {self.rate}'


class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
