from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from recipe_catalog.models import Recipe

User = get_user_model()

class TestRoutes(TestCase):
    RECIPE_NAME = 'Яичница'
    @classmethod
    def setUpTestData(cls):
        cls.recipe = Recipe.objects.create(name=cls.RECIPE_NAME,)
        cls.user = User.objects.create(username='testUser')
        cls.client_logged_in = Client()
        cls.client_logged_in.force_login(cls.user)

    def test_index_page(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_ok(self):
        url = reverse('recipe_detail', args=[self.recipe.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_ok(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)