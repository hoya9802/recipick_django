"""
Expiration APi 테스트
"""
import tempfile
import os
from PIL import Image

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.tests.test_recipe_api import create_user

from notification.models import Expiration
from notification.serializers import (
    ExpirationSerializer,
    ExpirationListSerializer
)


EXPIRATIONS_URL = reverse('notification:expiration-list')


def detail_url(expiration_id):
    """Expiration detail URL을 생성하고 반환"""
    return reverse('notification:expiration-detail', args=[expiration_id])


def create_expiration(**params):
    """유통기한을 만들고 해당 객체를 return"""
    defaults = {
        'title': 'expiration title',
        'description': 'expiration description',
    }
    defaults.update(params)

    return Expiration.objects.create(**defaults)


class PublicExpirationsApiTests(TestCase):
    """인증받지 못한 사람에 대한 테스트"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """재료를 가져올때 오류를 발생시키는지 테스트"""
        res = self.client.get(EXPIRATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateExpirationsApiTests(TestCase):
    """인증받은 유저에 대한 API요청 테스트"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.expiration = create_expiration(title='Test Expiration')

    def tearDown(self):
        self.expiration.image.delete()

    def test_retrieve_expiration(self):
        """유통기한들을 잘 가져오는지 테스트"""
        Expiration.objects.create(title='삼겹살')
        Expiration.objects.create(title='참치')

        res = self.client.get(EXPIRATIONS_URL)

        expirations = Expiration.objects.all().order_by('title')
        serializer = ExpirationListSerializer(expirations, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_expiration_detail(self):
        """유통기한의 디테일 정보를 잘 가져오는지 테스트"""
        expiration = Expiration.objects.create(title='삼겹살')

        url = detail_url(expiration.id)
        res = self.client.get(url)

        serializer = ExpirationSerializer(expiration)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_image_to_expiration(self):
        """유통기한 객체에 이미지를 가져오는지 테스트"""

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            temp_file_name = ntf.name

        expiration = Expiration.objects.create(
            title='삼겹살',
            image=temp_file_name,
            description='expiration description',
        )
        url = detail_url(expiration.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(res.data['image'].endswith(expiration.image.url))

        os.unlink(temp_file_name)
