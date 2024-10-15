from django.shortcuts import render
# Create your views here.

recipe_list = [
        {'title': "Pancakes with meat", 'recipe_id': 1},
        {'title': "Caesar salad", 'recipe_id': 2},
        {'title': "Risotto", 'recipe_id': 3}
]

def about(request):
    return render(request, 'recipe_catalog/about.html')


def index(request):
    template_name = 'recipe_catalog/index.html'

    context = {
        'recipe_list': recipe_list
    }
    return render(request, template_name, context)


def recipe_detail(request, pk):
    template_name = 'recipe_catalog/recipe.html'

    context = {
        'title': recipe_list[pk-1]['title'],
        'recipe_id': pk
    }
    return render(request, template_name, context)
