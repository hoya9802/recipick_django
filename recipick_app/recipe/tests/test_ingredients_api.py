"""
Ingredient APi 테스트
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    """Ingredient detail URL을 생성하고 반환"""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(id='user', nick_name='user1', email='test@example.com'):
    """유저를 만들고 해당 객체를 return"""

    return get_user_model().objects.create(
        id=id,
        password='testpass',
        nick_name=nick_name,
        email=email
    )


class PublicIngredientsApiTests(TestCase):
    """인증받지 못한 사람에 대한 테스트"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """재료를 가져올때 오류를 발생시키는지 테스트"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """인증받은 유저에 대한 API요청 테스트"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredient(self):
        """재료들을 잘 가져오는지 테스트"""
        Ingredient.objects.create(name='삼겹살')
        Ingredient.objects.create(name='참치')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_ingredient_detail(self):
        """재료의 디테일 정보를 잘 가져오는지 테스트"""
        ingredient = Ingredient.objects.create(name='삼겹살')

        url = detail_url(ingredient.id)
        res = self.client.get(url)

        serializer = IngredientSerializer(ingredient)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
