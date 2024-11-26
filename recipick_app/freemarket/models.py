import uuid
import os

from django.conf import settings
from django.db import models


def freemarket_image_file_path(instance, filename):
    """새로운 이미지에대한 경로 생성"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads', 'freemarket', filename)


class Freemarket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='freemarkets'
    )
    image = models.ImageField(null=True, upload_to=freemarket_image_file_path)
    name = models.CharField(max_length=100)
    purchase_dt = models.DateField(blank=False)
    count = models.PositiveSmallIntegerField(blank=False)
    is_shared = models.BooleanField(default=False)
    description = models.TextField(blank=False)
    create_dt = models.DateField(auto_now_add=True)
    modify_dt = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
