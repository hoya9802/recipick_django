'''from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me') #로그인된 사용자의 정보를 반환

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'id' : 'test',
            'password': 'testpass123',
            'nick_name': 'Test Name',
            'email': 'test@example.com',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(id=payload['id']) #생성된 사용자를 id로 가져옴
        self.assertTrue(user.check_password(payload['password'])) #비밀번호가 해시로 저장되었는지 확인
        self.assertNotIn('password', res.data) #응답할 때 비밀번호가 포함 안됐는지 확인

    def test_user_with_id_exists_error(self): #이미 존재하는 아이디로 가입했을 때 오류가 발생하는지
        payload = {
            'id' : 'test',
            'password': 'testpass123',
            'nick_name': 'Test Name',
            'email': 'test123@example.com',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self): #비밀번호가 너무 짧을 때 오류가 발생하는지
        payload = {
            'id' : 'test',
            'password': 'pw',
            'nick_name': 'Test Name',
            'email': 'test123@example.com',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # 비밀번호가 너무 짧아서 오류가 발생함, user가 생성 안됐는지 확인함
        user_exists = get_user_model().objects.filter(
            id=payload['id']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self): #인증 토큰이 생성 되는지
        user_details = {
            'id' : 'test',
            'password': 'test-user-password123',
            'nick_name': 'Test Name',
            'email': 'test@example.com',
        }
        create_user(**user_details)

        payload = {
            'id': user_details['id'],
            'email': user_details['email'],
            'password': user_details['password'],
        } #토큰 생성할 때 필요한 인증 정보
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data) #res.data에 'token'키가 있는지 확인
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self): #잘못된 인증으로 토큰 요청할 때 오류가 뜨는지 확인
        create_user(id='test',
                    email='test@example.com',
                    password='testpass')

        payload = {'id':'test',
                   'email': 'test@example.com',
                   'password': 'testnonpass'} #잘못된 비밀번호 입력
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_id_not_found(self): #존재하지 않는 아이디로 토큰 요청할 때
        payload = {'id': 'test', 'email': 'test@example.com', 'password': 'pass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self): #비밀번호가 빈 문자열일때 인증 토큰 요청
        payload = {'id': 'test', 'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self): #로그인 안한 사용자가 정보를 요청할 때
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):

    def setUp(self):
        self.user = create_user(
            id = 'test',
            password = 'testpass123',
            nick_name = 'Test Name',
            email = 'test@example.com',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self): #인증된 사용자가 본인의 정보를 볼 수 있는지 확인
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'id': self.user.id,
            'nick_name': self.user.nick_name,
            'email': self.user.email,
        }) #올바른 정보를 반환하는지 확인

    def test_post_me_not_allowed(self):
        res = self.client.post(ME_URL, {}) #빈데이터로 post요청

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)'''

