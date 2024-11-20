from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from recipe import models


def create_user(id='user', password='testpass'):
    """유저를 만들고 해당 객체를 return"""
    return get_user_model().objects.create(
        id=id,
        password=password,
        nick_name='user1',
        email='test@example.com',
    )


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

    recipe = models.Recipe.objects.create(user=user, **default)
    return recipe


class ModelTests(TestCase):

    def test_create_user_with_id_successful(self):
        # id로 유저를 성공적으로 생성할 수 있는지 확인

        id = 'test'
        password = 'testpass123'
        nick_name = 'abc'
        email = 'test@example.com'
        level = None
        profile_image = 'path/to/test_image.jpg'
        loc = 127

        user = get_user_model().objects.create_user(
            id=id,
            password=password,
            nick_name=nick_name,
            email=email,
            level=level,
            profile_image=profile_image,
            loc=loc
        )

        self.assertEqual(user.id, id)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_craete_recipe(self):
        """레시피 모델 성공적으로 만들어지는지 테스트"""

        user = create_user()
        recipe = models.Recipe.objects.create(
            user=user,
            name='spaghetti',
            time_minutes=20,
            serving=2,
            description='looks so good',
        )

        self.assertEqual(str(recipe), recipe.name)

    def test_create_category(self):
        """카테고리 모델 성공적으로 만들어지는 테스트"""
        category = models.Category.objects.create(
            name='양식'
        )

        self.assertEqual(str(category), category.name)

    def test_create_likeng(self):
        """likeng 모델이 성공적으로 만들어지는지 테스트"""
        new_user = create_user()
        recipe = create_recipe(user=new_user)
        likeng = models.LikeNg.objects.create(
            rater=new_user,
            recipe_rated=recipe,
            rate=1,
        )

        self.assertEqual(str(likeng), f"{likeng.recipe_rated} - {likeng.rate}")

    @patch('recipe.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """레시피 파일 이름이 uuid로 생성되는지 테스트"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')
        expected_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)
