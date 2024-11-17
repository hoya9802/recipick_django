"""
Tests for category APIs.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Category

from recipe.serializers import CategorySerializer


CATEGORY_URL = reverse('recipe:category-list')


class PublicCategoryApiTests(TestCase):
    """인증 받지 못한 유저의 API 요청 테스트"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """카테고리 가져오는 것에 대해서 인증요청을 하는지 테스트"""
        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryApiTests(TestCase):
    """인증받은 유저에 대한 API 요청 테스트"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            id='userid',
            password='testpass',
            nick_name='user1',
            email='test@example.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_categories(self):
        """카테고리 데이터들을 잘 가져오는지 테스트"""
        Category.objects.create(name='양식')
        Category.objects.create(name='중식')
        Category.objects.create(name='일식')

        res = self.client.get(CATEGORY_URL)

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
