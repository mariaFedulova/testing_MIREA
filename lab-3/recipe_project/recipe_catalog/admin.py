from django.contrib import admin

# Register your models here.

from .models import Ingredient, Recipe, RecipeIngredient


class IngredientInline(admin.StackedInline):
    """В рецепте есть ингредиенты"""
    model = RecipeIngredient
    extra = 5

class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ["name"]
admin.site.register(Recipe, RecipeAdmin)

class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name"]
admin.site.register(Ingredient, IngredientAdmin)