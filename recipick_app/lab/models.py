import uuid
import os

from django.conf import settings
from django.db import models


def lab_image_file_path(instance, filename):
    """새로운 이미지에대한 이미지 경로 생성"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads', 'lab', filename)


class Lab(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='labs'
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=lab_image_file_path)
    description = models.TextField(blank=False)
    ingredients = models.ManyToManyField('recipe.Ingredient')
    create_dt = models.DateField(auto_now_add=True)
    modify_dt = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lablikes'
    )
    exlog = models.ForeignKey(
        Lab,
        on_delete=models.CASCADE,
        related_name='lablikes'
    )

    def __str__(self):
        return f"{self.exlog} - {self.user}"
