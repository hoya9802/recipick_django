from django.contrib import admin

from .models import Expiration, Announcement

# Register your models here.
admin.site.register(Expiration)
admin.site.register(Announcement)
