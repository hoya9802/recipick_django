import os
import logging
from unittest.mock import patch
import requests

from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.tests.test_recipe_api import create_user


# 테스트 시작 전에 환경 변수와 로깅 레벨 설정
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
logging.getLogger("transformers").setLevel(logging.ERROR)


AICHEF_URL = reverse('chef_ai:generate-recipe')

# 테스트용 Mock 응답
MOCK_RUNPOD_RESPONSE = {
    'title': '김치찌개',
    'ingredients': ['김치', '돼지고기', '두부'],
    'method': '1. 물을 끓인다\n2. 김치를 넣는다\n3. 돼지고기를 넣는다'
}


class PublicAiChefAPITests(TestCase):
    """인증받지 못한 유저에게 API요청을 거절하는지 테스트"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        input_data = {'ingredients': ['mushrooms', 'cabbage', 'soy sauce']}
        res = self.client.post(AICHEF_URL, input_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAiChefAPITests(TestCase):
    """인증받은 유저의 API요청을 허가하는지 테스트"""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)
        self.payload = {'ingredients': ['mushroom', 'cabbage', 'soy sauce']}
        self.invalid_payload = {'ingredients': ""}

    @patch.dict(os.environ, {
        'RUNPOD_API_KEY': 'test_api_key',
        'RUNPOD_API_URL': 'http://test-runpod-url'
    })
    @patch('requests.post')
    def test_post_valid_data(self, mock_post):
        """올바른 데이터에 대해서 레시피생성이 잘 이루어지는지 테스트"""
        # Mock RunPod API 응답 설정
        mock_post.return_value.json.return_value = MOCK_RUNPOD_RESPONSE
        mock_post.return_value.raise_for_status = lambda: None

        res = self.client.post(AICHEF_URL, self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # RunPod API 호출 검증
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(
            call_args[1]['headers']['Authorization'],
            'Bearer test_api_key'
        )
        self.assertEqual(
            call_args[1]['json'],
            self.payload
        )

        # 응답 데이터 검증
        self.assertEqual(
            res.data['title'],
            MOCK_RUNPOD_RESPONSE['title']
        )
        self.assertEqual(
            res.data['ingredients'],
            MOCK_RUNPOD_RESPONSE['ingredients']
        )
        self.assertEqual(
            res.data['method'],
            MOCK_RUNPOD_RESPONSE['method']
        )

    def test_post_invalid_data(self):
        """데이터를 넣지 않으면 레시피가 생성되지 않는지 테스트"""
        res = self.client.post(AICHEF_URL, self.invalid_payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.dict(os.environ, {
        'RUNPOD_API_KEY': 'test_api_key',
        'RUNPOD_API_URL': 'http://test-runpod-url'
    })
    @patch('requests.post')
    def test_runpod_api_error(self, mock_post):
        """RunPod API 오류 발생 시 적절한 에러 응답을 반환하는지 테스트"""
        # API 오류 시뮬레이션
        mock_post.side_effect = requests.RequestException("API Error")

        res = self.client.post(AICHEF_URL, self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn('error', res.data)
        self.assertIn('AI 서비스 연결 오류', res.data['error'])
