from django.urls import reverse
from django.test import SimpleTestCase, TestCase

from rest_framework import status
from rest_framework.test import APIClient

from chef_ai.main import generate_recipe
from recipe.tests.test_recipe_api import create_user


AICHEF_URL = reverse('chef_ai:generate-recipe')


class AIGenerationTest(SimpleTestCase):
    def test_recipe_generation(self):
        """레시피 생성이 정상적으로 작동하는지 테스트"""
        ingredients = ["kimchi", "pork", "soy sauce"]

        try:
            result = generate_recipe(ingredients)
            # 결과가 JSON 형식인지 확인
            self.assertIn('title', result)
            self.assertIn('ingredients', result)
            self.assertIn('method', result)

        except Exception as e:
            self.fail(f'Recipe generation failed with error: {e}')


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

    def test_post_valid_data(self):
        """올바른 데이터에 대해서 레시피생성이 잘 이루어지는지 테스트"""
        res = self.client.post(AICHEF_URL, self.payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        for pd, rd in zip(self.payload['ingredients'], res.data['prompt']):
            self.assertEqual(pd, rd)

        self.assertIn('title', res.data)
        self.assertIn('ingredients', res.data)
        self.assertIn('method', res.data)

    def test_post_invalid_data(self):
        """데이터를 넣지 않으면 레시피가 생성되지 않는지 테스트"""
        res = self.client.post(AICHEF_URL, self.invalid_payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
