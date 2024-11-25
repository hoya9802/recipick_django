from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime

from recipe.models import Recipe
from lab.models import Lab
from freemarket.models import Freemarket


MYPAGE_URL = reverse('user:mypage')


def create_user(id='user', password='testpass'):
    """유저를 만들고 해당 객체를 return"""
    return get_user_model().objects.create(
        id=id,
        password=password,
        nick_name='user1',
        email='test@example.com',
    )


def create_recipe(user, **params):
    """간단한 레시피를 만들고 반환하는 함수"""
    default = {
        'name': 'Sample recipe',
        'time_minutes': 5,
        'serving': 5,
        'link': 'http://example.com',
        'description': 'sample description',
    }
    default.update(params)

    recipe = Recipe.objects.create(user=user, **default)
    return recipe


def create_lab(user, **params):
    """간단한 요리실험일지를 만들고 반환하는 함수"""
    default = {
        'title': 'Lab title',
        'description': 'Lab desc',
    }
    default.update(params)

    lab = Lab.objects.create(user=user, **default)
    return lab


def create_freemarket(user, **params):
    """자유시장 글을 만들고 반환하는 함수"""
    default = {
        'name': 'freemarket name',
        'purchase_dt': datetime.now().date(),
        'count': 100,
        'is_shared': False,
        'description': 'freemarket description',
    }
    default.update(params)

    freemarket = Freemarket.objects.create(user=user, **default)
    return freemarket


class MypageCountTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_user_recipe_count_success(self):
        # 로그인한 유저가 작성한 recipe의 개수 조회 확인
        create_recipe(
            user=self.user,
            name='Sample recipe1',
            time_minutes=10,
            serving=3,
            link='http://example1.com',
            description='sample description1',
        )

        create_recipe(
            user=self.user,
            name='Sample recipe2',
            time_minutes=20,
            serving=5,
            link='http://exampl2.com',
            description='sample description2',
        )

        res = self.client.get(MYPAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn('recipes_count', res.data)
        self.assertEqual(res.data['recipes_count'], 2)

    def test_user_labs_count_success(self):
        create_lab(
            user=self.user,
            title='Lab title1',
            description='Lab desc1',
        )

        create_lab(
            user=self.user,
            title='Lab title2',
            description='Lab desc2',
        )

        res = self.client.get(MYPAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn('labs_count', res.data)
        self.assertEqual(res.data['labs_count'], 2)

    def test_user_freemarket_count_success(self):
        # 로그인한 유저가 작성한 freemarket의 개수 조회 확인
        create_freemarket(
            user=self.user,
            name='freemarket name1',
            purchase_dt=datetime.now().date(),
            count=1000,
            is_shared=False,
            description='freemarket1 description',
        )

        create_freemarket(
            user=self.user,
            name='freemarket name2',
            purchase_dt=datetime.now().date(),
            count=4000,
            is_shared=False,
            description='freemarket2 description',
        )

        res = self.client.get(MYPAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn('freemarkets_count', res.data)
        self.assertEqual(res.data['freemarkets_count'], 2)
