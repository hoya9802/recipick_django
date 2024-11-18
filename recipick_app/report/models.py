from django.conf import settings
from django.db import models


class Reportpage(models.Model):
    reporter = models.ForeignKey(
                    settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
    )
    link = models.CharField(max_length=255)
    create_dt = models.DateField(auto_now_add=True)
    detail = models.TextField()

    class Meta:
        ordering = ['-create_dt']

    def __str__(self):
        return f"{self.reporter}"
