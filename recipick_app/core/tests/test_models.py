from datetime import datetime
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from recipe import models
from help.models import Help
from lab.models import Lab, Like
from freemarket.models import Freemarket
from notification.models import Expiration, Announcement


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


def create_lab(user, **params):
    """간단한 요리실험일지를 만들고 반환하는 함수"""
    default = {
        'title': 'Lab title',
        'description': 'Lab desc',
    }
    default.update(params)

    lab = Lab.objects.create(user=user, **default)
    return lab


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

    def test_create_ingredient(self):
        """재료가 성공적으로 만들어지는지 테스트"""
        ingredient = models.Ingredient.objects.create(
            name='Ingredient1'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    @patch('recipe.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """레시피 파일 이름이 uuid로 생성되는지 테스트"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')
        expected_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)

    def test_create_help(self):
        """지식인이 성공적으로 만들어지는 테스트"""
        helps = Help.objects.create(
            user=create_user(),
            title='지신인 제목',
            description='Sample Description'
        )

        self.assertEqual(str(helps), f"{helps.id} - {helps.title}")

    def test_create_lab(self):
        """요리실험실이 성공적으로 만들어지는지 테스트"""
        lab = Lab.objects.create(
            user=create_user(),
            title='newlab title',
            description='newlab description'
        )

        self.assertEqual(str(lab), lab.title)

    def test_create_like(self):
        new_user = create_user()
        lab = create_lab(user=new_user)

        like = Like.objects.create(
            user=new_user,
            exlog=lab
        )

        self.assertEqual(str(like), f"{like.exlog} - {like.user}")

    def test_create_freemarket(self):
        """무료나눔 모델이 성공적으로 만들어지는지 테스트"""
        freemarket = Freemarket.objects.create(
            user=create_user(),
            name='freemarket name',
            purchase_dt=datetime.now(),
            count=100,
            is_shared=False,
            description='freemarket description',
        )

        self.assertEqual(str(freemarket), freemarket.name)

    def test_create_expiration(self):
        """유통기한 모델이 성공적으로 만들어지는지 테스트"""
        expiration = Expiration.objects.create(
            title='expiration title',
            description='expiration description',
            url='http://example.com'
        )

        self.assertEqual(str(expiration), expiration.title)

    def test_create_announcement(self):
        """공지사항 모델이 성공적으로 만들어지는지 테스트"""
        announcement = Announcement.objects.create(
            title='announcement title',
            contents='announcement contents',
            announce_dt=datetime.now()
        )

        self.assertEqual(str(announcement), announcement.title)
