"""
URL mappings for the help app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import HelpViewSet


app_name = 'help'


router = DefaultRouter()
router.register('helps', HelpViewSet)


urlpatterns = [
    path('', include(router.urls))
]
