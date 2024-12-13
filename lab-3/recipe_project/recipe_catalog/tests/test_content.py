from django.test import TestCase
from django.urls import reverse
from recipe_catalog.models import Recipe, Ingredient, RecipeIngredient

class TestOneDb(TestCase):
    RECIPE_NAME = 'Яичница'
    INGREDIENT_NAME = 'Яйцо'

    @classmethod
    def setUpTestData(cls):
        cls.ingredient_egg = Ingredient.objects.create( name=cls.INGREDIENT_NAME,)
        cls.recipe = Recipe.objects.create(name= cls.RECIPE_NAME,)
        RecipeIngredient.objects.create(
            recipe=cls.recipe,
            ingredient=cls.ingredient_egg,
            weight=50,  # Вес в граммах
            count=0
        )
        cls.recipe.ingredients.set([cls.ingredient_egg])

    def test_successful_creation_ingredient(self):
        ingredients_count = Ingredient.objects.count()
        self.assertEqual(ingredients_count, 1)

    def test_successful_creation_recipe(self):
        recipe_count = Recipe.objects.count()
        self.assertEqual(recipe_count, 1)

    def test_successful_create_recipe_ingredient(self):
        counts = [
            (self.recipe.ingredients.count(), 1, "Рецепт"),
            (RecipeIngredient.objects.count(), 1, "Ингредиент-Рецепт"),
        ]
        for cnt in counts:
            with self.subTest(msg='Рецепты-ингредиенты'):
                self.assertEqual(cnt[0], cnt[1], cnt[2])

    def test_titles(self):
        titles = [
            (self.ingredient_egg.name, self.INGREDIENT_NAME, 'Ингредиент'),

            (self.recipe.name, self.RECIPE_NAME, 'Рецепт'),
        ]
        for name in titles:
            with self.subTest(msg=f'Название {name[2]}'):
                self.assertEqual(name[0], name[1])

    def test_recipe_detail_ingredients_order(self):
        response = self.client.get(
            reverse('recipe_detail', args=[self.recipe.id]))
        ingredients = response.context['ingredients']
        ingredient_names = [
            ingredient.ingredient.name for ingredient in ingredients]
        self.assertEqual(ingredient_names, sorted(ingredient_names))

    def test_recipe_ready_weight(self):
        response = self.client.get(
            reverse('recipe_detail', args=[self.recipe.id]))
        self.assertIsNotNone(response.context)
        expected_keys = ['title', 'recipe_url', 'recipe_id', 'steps', 'ingredients', 'ready_weight']
        for key in expected_keys:
            self.assertIn(key, response.context)
        total_weight = response.context['ready_weight']
        expected_weight = 50
        self.assertEqual(total_weight, expected_weight)
