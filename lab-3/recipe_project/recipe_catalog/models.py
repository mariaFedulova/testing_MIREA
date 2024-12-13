from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Ingredient(models.Model):
    """Составная часть рецепта."""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_name_unique",
                fields=["name"],
            ),
        ]

class Recipe(models.Model):
    """Рецепт."""
    name = models.CharField(max_length=300)
    url = models.CharField(max_length=300)
    description = models.CharField(max_length=1000, default="описание")
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    author = models.ForeignKey(User,
                               verbose_name='Автор рецепта',
                               on_delete=models.CASCADE, null=True
                               )

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_name_unique",
                fields=["name"],
            ),
        ]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    weight = models.IntegerField(default=0)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique recipes ingredients'
            ),
        ]
