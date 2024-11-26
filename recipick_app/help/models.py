import uuid
import os

from django.conf import settings
from django.db import models


def help_image_file_path(instance, filename):
    """새로운 이미지에대한 경로 생성"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads', 'help', filename)


class Help(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='help'
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=help_image_file_path)
    create_dt = models.DateField(auto_now_add=True)
    modify_dt = models.DateField(auto_now=True)
    description = models.TextField(blank=False)

    def __str__(self):
        return f"{self.id} - {self.title}"
