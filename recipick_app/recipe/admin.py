from django.contrib import admin
from recipe.models import Recipe, Category, LikeNg, Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Category)
admin.site.register(LikeNg)
