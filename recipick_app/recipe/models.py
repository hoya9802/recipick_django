from django.conf import settings
from django.db import models


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
    link = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    create_dt = models.DateField(auto_now_add=True)
    modify_dt = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
