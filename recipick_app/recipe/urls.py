"""
URL mappings for the recipe app.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    RecipeViewSet,
    CategoryListView,
    RecipesByCategoryListView,
    LikeNgViewSet,
    IngredientViewSet
)


router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('likengs', LikeNgViewSet)
router.register('ingredients', IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path(
        'categories/<int:category_id>/recipes/',
        RecipesByCategoryListView.as_view(),
        name='recipe-list-by-category'
    ),
]
