from django.contrib import admin
from recipe.models import Recipe, Category


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')


admin.site.register(Category)
