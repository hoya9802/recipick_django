from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

import os
import tempfile
from PIL import Image

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
PROFILE_URL = reverse('user:profile')
TEMP_MEDIA_ROOT = tempfile.mkdtemp()  # 임시 미디어 디렉토리 생성


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        # user가 생성되었는지 확인
        payload = {
            'id': 'test',
            'password': 'testpass123',
            'nick_name': 'Test Name',
            'email': 'test@example.com',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(id=payload['id'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_id_exists_error(self):
        # 이미 존재하는 아이디로 가입했을 때 오류가 발생하는지
        payload = {
            'id': 'test',
            'password': 'testpass123',
            'nick_name': 'Test Name',
            'email': 'test123@example.com',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        # 비밀번호가 너무 짧을 때 오류가 발생하는지
        payload = {
            'id': 'test',
            'password': 'pw',
            'nick_name': 'Test Name',
            'email': 'test123@example.com',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            id=payload['id']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        # 인증 토큰이 생성 되는지
        user_details = {
            'id': 'test',
            'password': 'test-user-password123',
            'nick_name': 'Test Name',
            'email': 'test@example.com',
        }
        create_user(**user_details)

        payload = {
            'id': user_details['id'],
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        # 잘못된 인증으로 토큰 요청할 때 오류가 뜨는지 확인
        create_user(id='test',
                    email='test@example.com',
                    password='testpass')

        payload = {'id': 'test',
                   'email': 'test@example.com',
                   'password': 'testnonpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_id_not_found(self):
        # 존재하지 않는 아이디로 토큰 요청할 때
        payload = {
                    'id': 'test',
                    'email': 'test@example.com',
                    'password': 'pass123'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        # 비밀번호가 빈 문자열일때 인증 토큰 요청
        payload = {'id': 'test', 'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        # 로그인 안한 사용자가 정보를 요청할 때
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):

    def setUp(self):
        self.user = create_user(
            id='test',
            password='testpass123',
            nick_name='Test Name',
            email='test@example.com',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        # 인증된 사용자가 본인의 정보를 볼 수 있는지 확인
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'id': self.user.id,
            'nick_name': self.user.nick_name,
            'email': self.user.email,
            'profile_image': None,
            'loc': None
        })

    def test_post_me_not_allowed(self):
        # ME_URL경로가 post요청을 처리하지 않는지 확인
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_delete_success(self):
        # 회원탈퇴가 제대로 되었는지 확인
        res = self.client.delete(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        user_exists = get_user_model().objects.filter(id=self.user.id).exists()
        self.assertFalse(user_exists)

    def tearDown(self):
        # 테스트 후 프로필 이미지 삭제
        if self.user.profile_image:
            self.user.profile_image.delete()

    def test_upload_profile_image(self):
        #  프로필 이미지를 성공적으로 업로드
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            # 10x10 크기의 임시 이미지 생성
            Image.new("RGB", (10, 10)).save(image_file, format="JPEG")
            image_file.seek(0)

            payload = {'profile_image': image_file}
            res = self.client.post(PROFILE_URL, payload, format='multipart')

        # 응답 상태 확인
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()

        # 이미지가 응답에 포함되었는지 확인
        self.assertIn('profile_image', res.data)
        self.assertTrue(os.path.exists(self.user.profile_image.path))
