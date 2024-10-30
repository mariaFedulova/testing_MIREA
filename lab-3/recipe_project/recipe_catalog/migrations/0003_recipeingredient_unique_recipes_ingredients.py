# Generated by Django 4.2.16 on 2024-10-30 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_catalog', '0002_recipeingredient_recipe_ingredients'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique recipes ingredients'),
        ),
    ]
