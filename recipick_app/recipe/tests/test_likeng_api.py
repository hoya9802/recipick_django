"""
Tests for LikeNg APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Recipe, LikeNg
from recipe.serializers import LikeNgSerializer


LIKENG_URL = reverse('recipe:likeng-list')


def detail_url(recipe_id):
    """Recipe id을 통한 디테일한 url을 리턴"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


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


def create_user(id='user', nick_name='user1', email='test@example.com'):
    """유저를 만들고 해당 객체를 return"""

    return get_user_model().objects.create(
        id=id,
        password='testpass',
        nick_name=nick_name,
        email=email
    )


class PublicRecipeAPITests(TestCase):
    """인증받지 못한 유저에 대한 요청 테스트"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """API를 호출할때 인증 필요여부 테스트"""
        res = self.client.get(LIKENG_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLikeNgAPITest(TestCase):
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

    def test_retrieve_likeng(self):
        """LikeNg 데이터들을 잘 가져오는지 테스트"""
        recipe = create_recipe(user=self.user)
        LikeNg.objects.create(
            rater=self.user,
            recipe_rated=recipe,
            rate=1
        )

        res = self.client.get(LIKENG_URL)

        likengs = LikeNg.objects.all()
        serializer = LikeNgSerializer(likengs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_like_recipe(self):
        """레시피에 좋아요가 작동하는지 테스트"""
        recipe = create_recipe(user=self.user)
        payload = {
            'recipe_rated': recipe.id,
            'rate': 1
        }
        res = self.client.post(LIKENG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LikeNg.objects.count(), 1)
        self.assertEqual(LikeNg.objects.get().rate, 1)

    def test_dislike_recipe(self):
        """레시피에 싫어요가 작동하는지 테스트"""
        recipe = create_recipe(user=self.user)
        payload = {
            'recipe_rated': recipe.id,
            'rate': -1
        }
        res = self.client.post(LIKENG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LikeNg.objects.count(), 1)
        self.assertEqual(LikeNg.objects.get().rate, -1)

    def test_toggle_like_dislike(self):
        """
        좋아요를 누른후 이후 싫어요를 누르면 이전데이터가 삭제되고,
        싫어요를 누른 데이터가 자동 생성되는지 테스트
        """
        recipe = create_recipe(user=self.user)
        payload = {
            'recipe_rated': recipe.id,
            'rate': 1
        }
        res = self.client.post(LIKENG_URL, payload)
        self.assertEqual(LikeNg.objects.count(), 1)

        payload = {
            'recipe_rated': recipe.id,
            'rate': -1
        }
        res = self.client.post(LIKENG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(LikeNg.objects.count(), 1)
        self.assertEqual(LikeNg.objects.get().rate, -1)

    def test_remove_like(self):
        """좋아요를 두번 누르면 올바르게 삭제가 되는지 테스트"""
        recipe = create_recipe(user=self.user)
        payload = {
            'recipe_rated': recipe.id,
            'rate': 1
        }
        self.client.post(LIKENG_URL, payload)
        self.assertEqual(LikeNg.objects.count(), 1)

        res = self.client.post(LIKENG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(LikeNg.objects.count(), 0)
