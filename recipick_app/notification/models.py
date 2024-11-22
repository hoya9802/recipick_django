import uuid
import os

from django.db import models


def expiration_image_file_path(instance, filename):
    """새로운 이미지에대한 경로 생성"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads', 'expiration', filename)


class Expiration(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=expiration_image_file_path)
    description = models.TextField(null=False)
    url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title}"


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    contents = models.TextField(null=False)
    announce_dt = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
