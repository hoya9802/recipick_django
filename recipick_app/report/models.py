from django.conf import settings
from django.db import models


class Status(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status


class Report(models.Model):
    reporter = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='reporter'
    )
    reported_user = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='reported_user',
                default=None
    )
    url = models.CharField(max_length=255)
    create_dt = models.DateField(auto_now_add=True)
    detail = models.TextField(blank=False)
    status = models.ForeignKey(
                'Status',
                on_delete=models.CASCADE,
                blank=True,
                null=True)

    class Meta:
        ordering = ['-create_dt']

    def __str__(self):
        return f"{self.reporter}"
