"""
URL mappings for the recipe app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    LabViewSet,
    LikeViewSet
)


router = DefaultRouter()
router.register('labs', LabViewSet)
router.register('likes', LikeViewSet)

app_name = 'lab'

urlpatterns = [
    path('', include(router.urls)),
]
