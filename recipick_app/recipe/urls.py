"""
URL mappings for the recipe app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, CategoryListView


router = DefaultRouter()
router.register('recipes', RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]