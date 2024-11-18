from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


class ReportpageAdmin(admin.ModelAdmin):
    ordering = ['-reporter']
    list_display = ['reporter', 'create_dt']
    fieldsets = (
        (_('Info'), {'fields': (
                        'reporter',
                        'link',
                        'create_dt',
                        'detail')}),
    )
    readonly_fields = ['reporter', 'link', 'create_dt', 'detail']


admin.site.register(models.Reportpage, ReportpageAdmin)
