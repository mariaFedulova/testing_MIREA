from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


from .models import Recipe, Ingredient, RecipeIngredient
from .forms import UserForm, IngredientForm, RecipeForm, RecipeIngredientForm
# Create your views here.

#recipe_list = [
#        {'title': "Pancakes with meat", 'recipe_id': 1, 'url_image': 'images/recipes/recipe1.jpg'},
#        {'title': "Caesar salad", 'recipe_id': 2, 'url_image': 'images/recipes/recipe2.jpg'},
#       {'title': "Risotto", 'recipe_id': 3, 'url_image': 'images/recipes/recipe3.jpg'}
#]

ADMIN_LOGIN = 'admin'

def about(request):
    return render(request, 'recipe_catalog/about.html')


def index(request):
    template_name = 'recipe_catalog/index.html'

    recipes = Recipe.objects.all().order_by('name')

    context = {
        'recipe_list': recipes
    }
    return render(request, template_name, context)


def recipe_detail(request, pk):
    template_name = 'recipe_catalog/recipe.html'

    recipe = Recipe.objects.get(pk=pk)

    ingredients = recipe.recipeingredient_set.all().order_by('ingredient__name')

    ready_weight = get_ready_weight(ingredients)

    context = {
        'title': recipe.name,
        'recipe_url': recipe.url,
        'recipe_id': pk,
        'steps': recipe.description,
        'ingredients': ingredients,
        'ready_weight': ready_weight,
        'author': recipe.author
    }
    return render(request, template_name, context)

def get_ready_weight(ingredients):
    result = 0
    for item in ingredients:
        result += item.weight
    return result

def form_user_test(request):
    """Тестовая форма для пользователя."""
    template_name = 'recipe_catalog/user_form_test.html'
    if request.GET:
        # создаём форму на основе параметров запроса.
        form = UserForm(request.GET)
        # Если данные валидны...
        if form.is_valid():
            # это тест - ничего в БД не заносим
            pass
    else:
        # Создаём экземпляр класса формы.
        form = UserForm()

    # Добавляем форму в словарь контекста:
    context = {'form': form}
    # создаём страницу по шаблону
    return render(request, template_name, context)

@login_required
def ingredient(request):
    if request.user.username != ADMIN_LOGIN:
        # Выдаём ошибку прав
        raise PermissionDenied
    """Форма для ингредиентов."""
    template = 'recipe_catalog/ingredient_form.html'
    form = IngredientForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        form.save()
        context = {'form': form}
    return render(request, template, context)

@login_required
def ingredient_edit(request, pk):
    """Форма для редактирования ингредиентов."""
    if request.user.username != ADMIN_LOGIN:
        # Выдаём ошибку прав
        raise PermissionDenied
    template = 'recipe_catalog/ingredient_form.html'
    # сначала нужно взять объект (если он есть)
    instance = get_object_or_404(Ingredient, pk=pk)
    # связываем форму с найденным объектом
    form = IngredientForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, template, context)

def ingredients(request):
    """Сформировать список ингредиентов."""
    template_name = 'recipe_catalog/ingredients.html'
    ingredients = Ingredient.objects.all().order_by('name')
    context = {
        'ingredient_list': ingredients
    }
    return render(request, template_name, context)

@login_required
def ingredient_delete(request, pk):
    """Форма для удаления ингредиента."""
    if request.user != ADMIN_LOGIN:
        # Выдаём ошибку прав
        raise PermissionDenied
    template = 'recipe_catalog/ingredient_form.html'
    instance = get_object_or_404(Ingredient, pk=pk)
    # В форму передаём только объект модели (форму не отображаем)
    form = IngredientForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('ingredients')
    # Если был получен GET-запрос — отображаем форму.
    return render(request, template, context)

@login_required
def recipe(request):
    form = RecipeForm(request.POST or None)
    template = 'recipe_catalog/recipe_form.html'
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()

    return render(request, template, context)


@login_required
def add_recipe_ingredient(request, pk):
    try:
        recipe = Recipe.objects.get(id=pk, author=request.user)
    except Recipe.DoesNotExist:
        raise Http404("Рецепт не найден/у Вас нет прав редактирования.")
    
    form = RecipeIngredientForm(request.POST or None)
    template = 'recipe_catalog/recipe_ingredient_form.html'
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.recipe = recipe
        instance.save()

    return render(request, template, context)


@login_required
def recipe_edit(request, pk):
    # Получаем нужный объект.
    instance = get_object_or_404(Recipe, pk=pk)
    ingredients = instance.recipeingredient_set.all().order_by('ingredient__name')
    # Проверяем, кто автор объекта.
    if instance.author != request.user:
        # Выдаём ошибку прав
        raise PermissionDenied
    form = RecipeForm(request.POST or None, instance=instance)
    template = 'recipe_catalog/recipe_form.html'
    context = {
                'form': form,
                'ingredients': ingredients,
            }
    if form.is_valid():
        print(form.data)
        instance = form.save(commit=False)
        instance.save()
        return redirect('index')

    return render(request, template, context)

@login_required
def recipe_delete(request, pk):
    # Получаем нужный объект.
    instance = get_object_or_404(Recipe, pk=pk)
    # Проверяем, кто автор объекта.
    if instance.author != request.user:
        # Выдаём ошибку прав
        raise PermissionDenied
    instance.delete()
    return redirect('index')

@login_required
def delete_recipe_ingredient(request, pk, ingredient_id):
    try:
        ingredient = RecipeIngredient.objects.get(
            id=ingredient_id, recipe__id=pk, recipe__author=request.user
        )
        ingredient.delete()
    except RecipeIngredient.DoesNotExist:
        raise Http404("Ингредиент не найден или недоступен.")

    return redirect('recipe_detail', pk=pk)


@login_required
def simple_view(request):
    return HttpResponse('Привет залогиненный пользователь!')