"""
URL mappings for the freemarket app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import FreemarketViewSet


app_name = 'freemarket'


router = DefaultRouter()
router.register('freemarkets', FreemarketViewSet)


urlpatterns = [
    path('', include(router.urls))
]
