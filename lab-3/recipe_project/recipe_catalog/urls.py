from django.urls import path, include
from django.contrib.auth import views
from .views import about, index, recipe_detail, form_user_test, ingredient, ingredient_edit, ingredient_delete, ingredients, recipe, add_recipe_ingredient, recipe_edit, recipe_delete, delete_recipe_ingredient

urlpatterns = [
    path('', index, name='index'),
    path('recipe/<int:pk>', recipe_detail, name='recipe_detail'),
    path('about', about, name='about'),
    path('user_form_test/', form_user_test, name='create_user_test'),
    path('ingredient/', ingredient, name='ingredient'),
    path('ingredient/<int:pk>/edit/', ingredient_edit, name='ingredient_edit'),
    path('ingredient/<int:pk>/delete/',ingredient_delete, name='ingredient_delete'),
    path('ingredients', ingredients, name='ingredients'),
    path('recipe/', recipe, name='recipe'),
    path('recipe/<int:pk>/edit/', recipe_edit, name='recipe_edit'),
    path('recipe/<int:pk>/add/', add_recipe_ingredient, name='recipe_add'),
    path('recipe/<int:pk>/delete/', recipe_delete, name='recipe_delete'),
    path('recipe/<int:pk>/delete/<int:ingredient_id>/', delete_recipe_ingredient, name='delete_recipe_ingredient'),
    path('auth/login/', views.LoginView.as_view(template_name='login.html'),name='login'),
    path('auth/logout/',views.LogoutView.as_view(), name='logout'),
]