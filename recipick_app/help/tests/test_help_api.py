"""
Tests for Help APIs.
"""
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Level

from help.models import Help
from help.serializers import (
    HelpSerializer,
    HelpListSerializer
)
from recipe.tests.test_recipe_api import create_user


HELP_URL = reverse('help:help-list')


def detail_url(help_id):
    """요리지식인 id을 통한 디테일한 url을 리턴"""
    return reverse('help:help-detail', args=[help_id])


def image_upload_url(help_id):
    """레시피 id를 통한 이미지 업로드 url을 리턴"""
    return reverse('help:help-upload-image', args=[help_id])


def create_help(user, **params):
    """지식인 글을 만들고 반환하는 함수"""
    default = {
        'title': 'Sample title',
        'description': 'Sample description'
    }
    default.update(params)

    help = Help.objects.create(user=user, **default)
    return help


class PublicHelpAPITests(TestCase):
    """인증받지 못한 유저에 대한 요청 테스트"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(HELP_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateHelpAPITests(TestCase):
    """인증받은 유저에 대한 API 요청 테스트"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_helps(self):
        """지식인글들을 잘 가져오는지 테스트"""
        create_help(user=self.user, title='Sample1')
        create_help(user=self.user, title='Sample2')

        res = self.client.get(HELP_URL)

        helps = Help.objects.all().order_by('-modify_dt')
        serializer = HelpListSerializer(helps, many=True)

        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_help_list_limited_to_user(self):
        """인증받은 유저의 지식인을 잘 가져오는지 테스트"""

        other_user = create_user(
            id='test1',
            nick_name='test1',
            email='test1@example.com'
        )

        create_help(user=other_user)
        create_help(user=self.user)

        res = self.client.get(HELP_URL)

        helps = Help.objects.filter(user=self.user)
        serializer = HelpListSerializer(helps, many=True)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_all_helps(self):
        """모든 유저들의 지식인을 잘 가져오는지 테스트"""

        other_user = create_user(
            id='test1',
            nick_name='test1',
            email='test1@example.com'
        )

        create_help(user=other_user)
        create_help(user=self.user)

        res = self.client.get(HELP_URL, {'all': 'true'})

        helps = Help.objects.all()
        serializer = HelpListSerializer(helps, many=True)

        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_helps_includes_user_nick_name(self):
        """지식인들을 가져올때 유저 닉네임을 가져오는지 테스트"""
        create_help(user=self.user)

        res = self.client.get(HELP_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = res.data[0]
        self.assertEqual(res['user']['nick_name'], self.user.nick_name)

    def test_get_help_detail(self):
        """지식인의 디테일한 내용을 가져오는지 테스트"""
        help = create_help(user=self.user)

        url = detail_url(help.id)

        res = self.client.get(url)

        serializer = HelpSerializer(help)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_other_user_help_detail(self):
        """다른유저가 만든 지식인글의 디테일한 내용을 가져오는지 테스트"""
        other_user = create_user(
            id='newuser',
            nick_name='newuser',
            email='newuser@example.com'
        )
        help = create_help(user=other_user)

        url = detail_url(help.id)
        res = self.client.get(url)

        serializer = HelpSerializer(help)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_help(self):
        """지식인이 실제로 만들어지는지 확인하는 테스트"""
        payload = {
            'title': 'test title',
            'description': 'test description'
        }
        res = self.client.post(HELP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        help = Help.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(help, k), v)
        self.assertEqual(help.user, self.user)

    def test_patial_update(self):
        """지식인의 특정 부분 업데이트가 가능한지 테스트"""
        help = create_help(
            user=self.user,
            title='test title',
            description='test description'
        )
        payload = {'title': 'New Help title'}
        url = detail_url(help.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        help.refresh_from_db()
        self.assertEqual(help.title, payload['title'])
        self.assertEqual(help.user, self.user)

    def test_full_update(self):
        """모든 지식인이 다 업데이트가 가능한지 테스트"""
        help = create_help(
            user=self.user,
            title='Sample title',
            description='Sample description'
        )
        payload = {
            'title': 'test title',
            'description': 'test description'
        }
        url = detail_url(help.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        help.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(help, k), v)
        self.assertEqual(help.user, self.user)

    def test_update_user_returns_error(self):
        """지식인의 유저이름을 변경할 수 없다는 것을 테스트"""
        new_user = create_user(
            id='new_user',
            nick_name='new_user',
            email='new@example.com'
        )
        help = create_help(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(help.id)
        self.client.patch(url, payload)

        help.refresh_from_db()
        self.assertEqual(help.user, self.user)

    def test_delete_recipe(self):
        """지식인이 성공적으로 삭제되는지 테스트"""
        help = create_help(user=self.user)

        url = detail_url(help.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Help.objects.filter(id=help.id).exists())

    def test_delete_other_users_recipe_error(self):
        """다른 유저들은 해당유저의 지식인을 삭제할 수 없다는 것을 테스트"""
        new_user = create_user(
            id='new_user',
            nick_name='new_user',
            email='new@example.com'
        )
        help = create_help(user=new_user)

        url = detail_url(help.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Help.objects.filter(id=help.id).exists())


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
        self.help = create_help(user=self.user)

    def tearDown(self):
        self.help.image.delete()

    def test_upload_image(self):
        """이미지 업로드 테스트"""
        url = image_upload_url(self.help.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.help.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.help.image.path))

    def test_upload_image_to_recipe(self):
        """지식인에 이미지를 업로드하는 테스트"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                'title': 'help me!! test',
                'description': 'Sample Description',
                'image': image_file,
            }
            res = self.client.post(HELP_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', res.data)

        # Get the newly created recipe
        new_help = Help.objects.get(id=res.data['id'])
        self.assertTrue(os.path.exists(new_help.image.path))

    def test_update_recipe_with_image(self):
        """기존 이미지에 대해서 레시피를 업데이트하는 테스트"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                'title': 'help me!! test',
                'description': 'Sample Description',
                'image': image_file,
            }
            res = self.client.post(HELP_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        url = detail_url(res.data['id'])
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (20, 20)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.patch(url, payload, format='multipart')

        self.help.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        new_help = Help.objects.get(id=res.data['id'])
        self.assertTrue(os.path.exists(new_help.image.path))

    def test_upload_image_bad_request(self):
        """잘못된 요청으로 이미지 업로드 테스트"""
        url = image_upload_url(self.help.id)
        payload = {'image': 'notimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
