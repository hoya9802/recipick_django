"""
URL mappings for the notification app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import AnnouncementViewSet, ExpirationViewSet


app_name = 'notification'


router = DefaultRouter()
router.register('announcements', AnnouncementViewSet)
router.register('expirations', ExpirationViewSet)


urlpatterns = [
    path('', include(router.urls))
]
