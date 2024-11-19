from django.contrib import admin
from .models import Report, Status


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'reported_user', 'status', 'create_dt')
    search_fields = ('reporter', 'reported_user')
    list_filter = ('create_dt',)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status', )
