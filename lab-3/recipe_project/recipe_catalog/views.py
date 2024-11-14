from django.shortcuts import render

from .models import Recipe
# Create your views here.

recipe_list = [
        {'title': "Pancakes with meat", 'recipe_id': 1, 'url_image': 'images/recipes/recipe1.jpg'},
        {'title': "Caesar salad", 'recipe_id': 2, 'url_image': 'images/recipes/recipe2.jpg'},
        {'title': "Risotto", 'recipe_id': 3, 'url_image': 'images/recipes/recipe3.jpg'}
]

def about(request):
    return render(request, 'recipe_catalog/about.html')


def index(request):
    template_name = 'recipe_catalog/index.html'

    recipes = Recipe.objects.all()

    context = {
        'recipe_list': recipes
    }
    return render(request, template_name, context)


def recipe_detail(request, pk):
    template_name = 'recipe_catalog/recipe.html'

    recipe = Recipe.objects.get(pk=pk)

    context = {
        'title': recipe.name,
        'recipe_url': recipe.url,
        'recipe_id': pk,
        'ingredients': recipe.recipeingredient_set.all().order_by('ingredient__name')
    }
    return render(request, template_name, context)