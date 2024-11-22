"""
Tests for Freemarket APIs.
"""
from datetime import datetime
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Level

from freemarket.models import Freemarket
from freemarket.serializers import (
    FreemarketSerializer,
    FreemarketListSerializer
)
from recipe.tests.test_recipe_api import create_user


FREEMARKET_URL = reverse('freemarket:freemarket-list')


def detail_url(freemarket_id):
    """자유시장 id을 통한 디테일한 u rl을 리턴"""
    return reverse('freemarket:freemarket-detail', args=[freemarket_id])


def image_upload_url(freemarket_id):
    """자유시장 id를 통한 이미지 업로드 url을 리턴"""
    return reverse('freemarket:freemarket-upload-image', args=[freemarket_id])


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


class PublicHelpAPITests(TestCase):
    """인증받지 못한 유저에 대한 요청 테스트"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FREEMARKET_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateHelpAPITests(TestCase):
    """인증받은 유저에 대한 API 요청 테스트"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_freemarkets(self):
        """자유시장글들을 잘 가져오는지 테스트"""
        create_freemarket(user=self.user, name='Sample1')
        create_freemarket(user=self.user, name='Sample2')

        res = self.client.get(FREEMARKET_URL)

        freemarkets = Freemarket.objects.all().order_by('-modify_dt')
        serializer = FreemarketListSerializer(freemarkets, many=True)

        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_freemarket_list_limited_to_user(self):
        """인증받은 유저의 자유시장을 잘 가져오는지 테스트"""

        other_user = create_user(
            id='test1',
            nick_name='test1',
            email='test1@example.com'
        )

        create_freemarket(user=other_user)
        create_freemarket(user=self.user)

        res = self.client.get(FREEMARKET_URL)

        freemarkets = Freemarket.objects.filter(user=self.user)
        serializer = FreemarketListSerializer(freemarkets, many=True)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_all_freemarkets(self):
        """모든 유저들의 자유시장을 잘 가져오는지 테스트"""

        other_user = create_user(
            id='test1',
            nick_name='test1',
            email='test1@example.com'
        )

        create_freemarket(user=other_user)
        create_freemarket(user=self.user)

        res = self.client.get(FREEMARKET_URL, {'all': 'true'})

        freemarkets = Freemarket.objects.all()
        serializer = FreemarketListSerializer(freemarkets, many=True)

        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_freemarkets_includes_user_nick_name(self):
        """자유시장들을 가져올때 유저 닉네임을 가져오는지 테스트"""
        create_freemarket(user=self.user)

        res = self.client.get(FREEMARKET_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = res.data[0]
        self.assertEqual(res['user']['nick_name'], self.user.nick_name)

    def test_get_freemarket_detail(self):
        """자유시장의 디테일한 내용을 가져오는지 테스트"""
        freemarket = create_freemarket(user=self.user)

        url = detail_url(freemarket.id)

        res = self.client.get(url)

        serializer = FreemarketSerializer(freemarket)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_other_user_freemarket_detail(self):
        """다른유저가 만든 자유시장글의 디테일한 내용을 가져오는지 테스트"""
        other_user = create_user(
            id='newuser',
            nick_name='newuser',
            email='newuser@example.com'
        )
        freemarket = create_freemarket(user=other_user)

        url = detail_url(freemarket.id)
        res = self.client.get(url)

        serializer = FreemarketSerializer(freemarket)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_freemarket(self):
        """자유시장이 실제로 만들어지는지 확인하는 테스트"""
        payload = {
            'name': 'test name',
            'purchase_dt': datetime.strptime('2022-11-20', '%Y-%m-%d').date(),
            'count': 100,
            'is_shared': False,
            'description': 'test description',
        }
        res = self.client.post(FREEMARKET_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        freemarket = Freemarket.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(freemarket, k), v)
        self.assertEqual(freemarket.user, self.user)

    def test_patial_update(self):
        """자유시장의 특정 부분 업데이트가 가능한지 테스트"""
        freemarket = create_freemarket(
            user=self.user,
            name='test name',
            description='test description'
        )
        payload = {'name': 'New Freemarket name'}
        url = detail_url(freemarket.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        freemarket.refresh_from_db()
        self.assertEqual(freemarket.name, payload['name'])
        self.assertEqual(freemarket.user, self.user)

    def test_full_update(self):
        """모든 자유시장이 다 업데이트가 가능한지 테스트"""
        freemarket = create_freemarket(
            user=self.user,
            name='Sample name',
            description='Sample description'
        )
        payload = {
            'name': 'New Freemarket name',
            'purchase_dt': datetime.strptime('2022-11-20', '%Y-%m-%d').date(),
            'count': 100,
            'is_shared': False,
            'description': 'New Freemarket description'
        }
        url = detail_url(freemarket.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        freemarket.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(freemarket, k), v)
        self.assertEqual(freemarket.user, self.user)

    def test_update_user_returns_error(self):
        """자유시장의 유저이름을 변경할 수 없다는 것을 테스트"""
        new_user = create_user(
            id='new_user',
            nick_name='new_user',
            email='new@example.com'
        )
        freemarket = create_freemarket(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(freemarket.id)
        self.client.patch(url, payload)

        freemarket.refresh_from_db()
        self.assertEqual(freemarket.user, self.user)

    def test_delete_freemarket(self):
        """자유시장이 성공적으로 삭제되는지 테스트"""
        freemarket = create_freemarket(user=self.user)

        url = detail_url(freemarket.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Freemarket.objects.filter(id=freemarket.id).exists())

    def test_delete_other_users_freemarket_error(self):
        """다른 유저들은 해당유저의 지식인을 삭제할 수 없다는 것을 테스트"""
        new_user = create_user(
            id='new_user',
            nick_name='new_user',
            email='new@example.com'
        )
        freemarket = create_freemarket(user=new_user)

        url = detail_url(freemarket.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Freemarket.objects.filter(id=freemarket.id).exists())


class ImageUploadTests(TestCase):
    """이미지 업로드 테스트"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            id='userid',
            password='testpass',
            nick_name='user1',
            email='test@example.com',
            level=Level.objects.create(name='Master Chef')
        )
        self.client.force_authenticate(user=self.user)
        self.freemarket = create_freemarket(user=self.user)

    def tearDown(self):
        self.freemarket.image.delete()

    def test_upload_image(self):
        """이미지 업로드 테스트"""
        url = image_upload_url(self.freemarket.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.freemarket.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.freemarket.image.path))

    def test_upload_image_to_freemarket(self):
        """자유시장에 이미지를 업로드하는 테스트"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                'name': 'freemarket name',
                'purchase_dt': datetime.now().date(),
                'count': 100,
                'is_shared': False,
                'description': 'freemarket description',
                'image': image_file,
            }
            res = self.client.post(FREEMARKET_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', res.data)

        # Get the newly created recipe
        new_freemarket = Freemarket.objects.get(id=res.data['id'])
        self.assertTrue(os.path.exists(new_freemarket.image.path))

    def test_update_freemarket_with_image(self):
        """기존 이미지에 대해서 자유시장을 업데이트하는 테스트"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                'name': 'freemarket name',
                'purchase_dt': datetime.now().date(),
                'count': 100,
                'is_shared': False,
                'description': 'freemarket description',
                'image': image_file,
            }
            res = self.client.post(FREEMARKET_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        url = detail_url(res.data['id'])
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (20, 20)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.patch(url, payload, format='multipart')

        self.freemarket.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        new_freemarket = Freemarket.objects.get(id=res.data['id'])
        self.assertTrue(os.path.exists(new_freemarket.image.path))

    def test_upload_image_bad_request(self):
        """잘못된 요청으로 이미지 업로드 테스트"""
        url = image_upload_url(self.freemarket.id)
        payload = {'image': 'notimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
