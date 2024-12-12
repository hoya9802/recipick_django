"""
URL mappings for the recipe app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    LabViewSet,
    LikeViewSet,
    LabByIngredientView,
)


router = DefaultRouter()
router.register('labs', LabViewSet)
router.register('likes', LikeViewSet)

app_name = 'lab'

urlpatterns = [
    path('', include(router.urls)),
    path(
        'ingredients/<int:ingredient_id>/labs/',
        LabByIngredientView.as_view(),
        name='lab-list-by-ingredient'
    ),
]
