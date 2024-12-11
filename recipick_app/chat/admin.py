from django.contrib import admin

from .models import ChatRoom, Message

# Register your models here.
@admin.register(ChatRoom)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop_user', 'visitor_user')


admin.site.register(Message)
