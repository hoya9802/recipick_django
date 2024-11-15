from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'email', 'nick_name', 'level']
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        (_('Info'), {'fields': (
                        'nick_name',
                        'profile_image',
                        'level',
                        'loc')}),
        (_('Permissions'), {'fields': (
                                'is_active',
                                'is_staff',
                                'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'id',
                'email',
                'password1',
                'password2',
                'nick_name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Level)

