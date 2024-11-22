"""
Tests for lab APIs.
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
from recipe.models import Ingredient
from lab.models import Lab, Like
from recipe.tests.test_recipe_api import create_user

from lab.serializers import (
    LabListSerializer,
    LabSerializer
)


LAB_URL = reverse('lab:lab-list')


def detail_url(lab_id):
    """Lab id을 통한 디테일한 url을 리턴"""
    return reverse('lab:lab-detail', args=[lab_id])


def image_upload_url(lab_id):
    """Lab id를 통한 이미지 업로드 url을 리턴"""
    return reverse('lab:lab-upload-image', args=[lab_id])


def create_lab(user, **params):
    """간단한 연구일지를 만들고 반환하는 함수"""
    default = {
        'title': 'Sample Lab title',
        'description': 'Simple Lab desc'
    }
    default.update(params)

    lab = Lab.objects.create(user=user, **default)
    return lab


class PublicLabAPITests(TestCase):
    """인증받지 못한 유저에 대한 요청 테스트"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """API를 호출할때 인증 필요여부 테스트"""
        res = self.client.get(LAB_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLabAPITest(TestCase):
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

    def test_retrieve_labs(self):
        """실험일지 데이터들을 잘 가져오는지 테스트"""
        create_lab(user=self.user, title='Apple Pie juice')
        create_lab(user=self.user, title='Shin Ramen cake')

        res = self.client.get(LAB_URL)

        labs = Lab.objects.all().order_by('-modify_dt')
        serializer = LabListSerializer(labs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_lab_list_limited_to_user(self):
        """인증받은 유저의 실험일지을 잘 가져오는지 테스트"""

        other_user = create_user(
            id='test1',
            nick_name='test1',
            email='test1@example.com'
        )

        create_lab(user=other_user)
        create_lab(user=self.user)

        res = self.client.get(LAB_URL)

        labs = Lab.objects.filter(user=self.user)
        serializer = LabListSerializer(labs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_all_labs(self):
        """모든 유저들의 실험일지을 잘 가져오는지 테스트"""

        other_user = create_user(
            id='test1',
            nick_name='test1',
            email='test1@example.com'
        )

        create_lab(user=other_user)
        create_lab(user=self.user)

        res = self.client.get(LAB_URL, {'all': 'true'})

        labs = Lab.objects.all()
        serializer = LabListSerializer(labs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_labs_includes_user_nick_name(self):
        """실험일지들을 가져올때 유저 닉네임을 가져오는지 확인"""
        create_lab(user=self.user)

        res = self.client.get(LAB_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = res.data[0]
        self.assertEqual(res['user']['nick_name'], self.user.nick_name)

    def test_get_lab_detail(self):
        """실험일지의 디테일한 내용을 가져오는지 테스트"""
        lab = create_lab(user=self.user)

        url = detail_url(lab.id)
        res = self.client.get(url)

        serializer = LabSerializer(lab)
        self.assertEqual(res.data, serializer.data)

    def test_get_other_user_lab_detail(self):
        """다른유저가 만든 실험일지의 디테일한 내용을 가져오는지 테스트"""
        other_user = create_user(
            id='newuser',
            nick_name='newuser',
            email='newuser@example.com'
        )
        lab = create_lab(user=other_user)

        url = detail_url(lab.id)
        res = self.client.get(url)

        serializer = LabSerializer(lab)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_lab(self):
        """실험일지가 실제로 만들어지는 확인하는 테스트"""
        payload = {
            'title': 'party noodle salad',
            'description': 'Sample Description'
        }
        res = self.client.post(LAB_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        lab = Lab.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(lab, k), v)
        self.assertEqual(lab.user, self.user)

    def test_partial_update(self):
        """실험일지의 특정 부분 업데이트가 가능한지 테스트"""
        lab = create_lab(
            user=self.user,
            title='Kimchi chicken',
            description='Sample Description'
        )
        payload = {'title': 'New lab name'}
        url = detail_url(lab.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        lab.refresh_from_db()
        self.assertEqual(lab.title, payload['title'])
        self.assertEqual(lab.user, self.user)

    def test_full_update(self):
        """모든 실험일지가 다 업데이트가 가능한지 테스트"""
        lab = create_lab(
            user=self.user,
            title='Kimchi noodle soup',
            description='Sample Description'
        )

        payload = {
            'title': 'Chicken Burger noodle',
            'description': "Mom's touch Burger i like"
        }
        url = detail_url(lab.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        lab.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(lab, k), v)
        self.assertEqual(lab.user, self.user)

    def test_update_user_returns_error(self):
        """실험일지의 유저이름을 변경할 수 없다는 것을 스트"""
        new_user = create_user(
            id='new_user',
            nick_name='new_user',
            email='new@example.com'
        )
        lab = create_lab(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(lab.id)
        self.client.patch(url, payload)

        lab.refresh_from_db()
        self.assertEqual(lab.user, self.user)

    def test_delete_lab(self):
        """실험일지가 성공적으로 삭제되는지 테스트"""
        lab = create_lab(user=self.user)

        url = detail_url(lab.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lab.objects.filter(id=lab.id).exists())

    def test_delete_other_users_lab_error(self):
        """다른 유저들은 해당유저의 실험일지을 삭제할 수 없다는 것을 테스트"""
        new_user = create_user(
            id='new_user',
            nick_name='new_user',
            email='new@example.com'
        )
        lab = create_lab(user=new_user)

        url = detail_url(lab.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Lab.objects.filter(id=lab.id).exists())

    def test_labs_includes_user_level(self):
        """실험일지를 가져올 때 유저의 칭호(level)를 가져오는지 확인"""

        level = Level.objects.create(name='Master Chef')
        self.user.level = level
        self.user.save()

        create_lab(user=self.user, title='Spaghetti Bolognese')

        res = self.client.get(LAB_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('user', res.data[0])
        self.assertIn('level', res.data[0]['user'])
        self.assertEqual(res.data[0]['user']['level'], 'Master Chef')

    def test_lab_serializer_likes_count(self):
        """실험일지에 Like를 카운팅 해주는지 테스트"""
        lab = create_lab(user=self.user)

        Like.objects.create(
            user=self.user,
            exlog=lab,
        )
        res = self.client.get(LAB_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = LabListSerializer(lab)
        self.assertEqual(res.data[0], serializer.data)
        self.assertEqual(serializer.data['likes_count'], 1)

    def test_create_lab_with_existing_ingredient(self):
        """기존에 존재하는 재료들을 바탕으로 실험일지를 만드는지 테스트"""
        # 미리 재료들을 생성
        Ingredient.objects.create(name='Lemon')
        Ingredient.objects.create(name='Fish Sauce')
        Ingredient.objects.create(name='Dragon')

        payload = {
            'title': 'party noodle soup',
            'description': 'Sample Description',
            'ingredients': [
                {'name': 'Lemon'},
                {'name': 'Fish Sauce'},
                {'name': 'Dragon'}
            ]
        }
        res = self.client.post(LAB_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        labs = Lab.objects.all()
        self.assertEqual(labs.count(), 1)
        lab = labs[0]
        self.assertEqual(lab.ingredients.count(), 3)

        for ingredient in payload['ingredients']:
            exists = lab.ingredients.filter(
                name=ingredient['name']
            ).exists()
            self.assertTrue(exists)

    def test_create_lab_with_non_existing_ingredient_error(self):
        """존재하지 않는 재료로 실험일지를 만들려고 할 때 에러가 발생하는지 테스트"""
        Ingredient.objects.create(name='Lemon')

        payload = {
            'name': 'party noodle',
            'time_minutes': 30,
            'serving': 2,
            'link': 'http://example.com',
            'description': 'Sample Description',
            'ingredients': [
                {'name': 'Lemon'},
                {'name': 'NonExistingIngredient'}
            ]
        }
        res = self.client.post(LAB_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lab.objects.count(), 0)

    def test_update_lab_assign_ingredient(self):
        """할당된 재료를 바탕으로 업데이트하는지 테스트"""
        # 미리 재료들을 생성
        ingredient1 = Ingredient.objects.create(name='Pepper')
        ingredient2 = Ingredient.objects.create(name='Chili')

        lab = create_lab(user=self.user)
        lab.ingredients.add(ingredient1)

        payload = {'ingredients': [{'name': 'Chili'}]}
        url = detail_url(lab.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        lab.refresh_from_db()  # DB에서 최신 데이터를 다시 불러옴
        self.assertIn(ingredient2, lab.ingredients.all())
        self.assertNotIn(ingredient1, lab.ingredients.all())

    def test_update_lab_with_non_existing_ingredient_error(self):
        """존재하지 않는 재료로 실험일지를 업데이트하려고 할 때 에러가 발생하는지 테스트"""
        ingredient = Ingredient.objects.create(name='Pepper')
        lab = create_lab(user=self.user)
        lab.ingredients.add(ingredient)

        payload = {'ingredients': [{'name': 'NonExistingIngredient'}]}
        url = detail_url(lab.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(ingredient, lab.ingredients.all())

    def test_clear_lab_ingredients(self):
        """레시피 재료들을 다 정리할 수 있는지 테스트"""
        ingredient = Ingredient.objects.create(name='Garlic')
        lab = create_lab(user=self.user)
        lab.ingredients.add(ingredient)

        payload = {'ingredients': []}
        url = detail_url(lab.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(lab.ingredients.count(), 0)


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
        self.lab = create_lab(user=self.user)

    def tearDown(self):
        self.lab.image.delete()

    def test_upload_image(self):
        """이미지 업로드 테스트"""
        url = image_upload_url(self.lab.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.lab.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.lab.image.path))

    def test_upload_image_to_lab(self):
        """실험일지에 이미지를 업로드하는 테스트"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                'title': 'trust me!! test',
                'description': 'Sample Description',
                'image': image_file,
            }
            res = self.client.post(LAB_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', res.data)

        # Get the newly created recipe
        new_lab = Lab.objects.get(id=res.data['id'])
        self.assertTrue(os.path.exists(new_lab.image.path))

    def test_update_lab_with_image(self):
        """기존 이미지에 대해서 요리실험일지를 업데이트하는 테스트"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                'title': 'trust me!! test',
                'description': 'Sample Description',
                'image': image_file,
            }
            res = self.client.post(LAB_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        url = detail_url(res.data['id'])
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (20, 20)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.patch(url, payload, format='multipart')

        self.lab.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        new_lab = Lab.objects.get(id=res.data['id'])
        self.assertTrue(os.path.exists(new_lab.image.path))

    def test_upload_image_bad_request(self):
        """잘못된 요청으로 이미지 업로드 테스트"""
        url = image_upload_url(self.lab.id)
        payload = {'image': 'notimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
