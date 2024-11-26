"""
Tests for Like APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from lab.models import Like
from lab.serializers import LikeSerializer

from lab.tests.test_lab_api import create_lab


LIKE_URL = reverse('lab:like-list')


class PublicRecipeAPITests(TestCase):
    """인증받지 못한 유저에 대한 요청 테스트"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """API를 호출할때 인증 필요여부 테스트"""
        res = self.client.get(LIKE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLikeAPITest(TestCase):
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

    def test_retrieve_like(self):
        """Like 데이터들을 잘 가져오는지 테스트"""
        lab = create_lab(user=self.user)
        Like.objects.create(
            user=self.user,
            exlog=lab,
        )

        res = self.client.get(LIKE_URL)

        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_like_lab(self):
        """실험일지에 좋아요가 작동하는지 테스트"""
        lab = create_lab(user=self.user)
        payload = {
            'exlog': lab.id,
        }
        res = self.client.post(LIKE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_remove_like(self):
        """좋아요를 두번 누르면 올바르게 삭제가 되는지 테스트"""
        lab = create_lab(user=self.user)
        payload = {
            'exlog': lab.id,
        }
        self.client.post(LIKE_URL, payload)
        self.assertEqual(Like.objects.count(), 1)

        res = self.client.post(LIKE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)
