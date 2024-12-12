"""
URL mappings for the help app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import HelpViewSet, CommentViewSet

app_name = 'help'

router = DefaultRouter()
router.register('helps', HelpViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
