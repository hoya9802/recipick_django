"""
Tests for recipe APIs.
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
from recipe.models import Recipe, Category, LikeNg, Ingredient

from recipe.serializers import RecipeSerializer, RecipeListSerializer


RECIPE_URL = reverse('recipe:recipe-list')
CATEGORY_URL = reverse('recipe:category-list')


def detail_url(recipe_id):
    """Recipe id을 통한 디테일한 url을 리턴"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def image_upload_url(recipe_id):
    """레시피 id를 통한 이미지 업로드 url을 리턴"""
    return reverse('recipe:recipe-upload-image', args=[recipe_id])


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

    recipe = Recipe.objects.create(user=user, **default)
    return recipe


def create_user(id='user', nick_name='user1', email='test@example.com'):
    """유저를 만들고 해당 객체를 return"""

    return get_user_model().objects.create(
        id=id,
        password='testpass',
        nick_name=nick_name,
        email=email
    )


def create_temp_image():
    """임시 이미지를 생성하는 함수"""
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=True)
    image = Image.new('RGB', (100, 100), color='red')
    image.save(temp_file, format='JPEG')
    temp_file.seek(0)
    return temp_file


class PublicRecipeAPITests(TestCase):
    """인증받지 못한 유저에 대한 요청 테스트"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """API를 호출할때 인증 필요여부 테스트"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):
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

    def test_retrieve_recipes(self):
        """레시피 데이터들을 잘 가져오는지 테스트"""
        create_recipe(user=self.user, name='Apple Pie')
        create_recipe(user=self.user, name='Shin Ramen')

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('-modify_dt')
        serializer = RecipeListSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """인증받은 유저의 레시피를 잘 가져오는지 테스트"""

        other_user = create_user(
            id='test1',
            nick_name='test1',
            email='test1@example.com'
        )

        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeListSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_all_recipes(self):
        """모든 유저들의 레시피를 잘 가져오는지 테스트"""

        other_user = create_user(
            id='test1',
            nick_name='test1',
            email='test1@example.com'
        )

        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL, {'all': 'true'})

        recipes = Recipe.objects.all()
        serializer = RecipeListSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_includes_user_nick_name(self):
        """레시피들을 가져올때 유저 닉네임을 가져오는지 확인"""
        create_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = res.data[0]
        self.assertEqual(res['user']['nick_name'], self.user.nick_name)

    def test_get_recipe_detail(self):
        """레시피의 디테일한 내용을 가져오는지 테스트"""
        recipe = create_recipe(user=self.user,
                               )

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_get_other_user_recipe_detail(self):
        """다른유저가 만든 레시피의 디테일한 내용을 가져오는지 테스트"""
        other_user = create_user(
            id='newuser',
            nick_name='newuser',
            email='newuser@example.com'
        )
        recipe = create_recipe(user=other_user)

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """레시피가 실제로 만들어지는 확인하는 테스트"""
        payload = {
            'name': 'party noodle',
            'time_minutes': 30,
            'serving': 2,
            'link': 'http://example.com',
            'description': 'Sample Description'
        }
        res = self.client.post(RECIPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """레시피의 특정 부분 업데이트가 가능한지 테스트"""
        recipe = create_recipe(
            user=self.user,
            name='Kimchi soup',
            time_minutes=15,
            serving=4,
            link='http://example.com',
            description='Sample Description'
        )
        payload = {'name': 'New recipe name'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """모든 레시피가 다 업데이트가 가능한지 테스트"""
        recipe = create_recipe(
            user=self.user,
            name='Kimchi soup',
            time_minutes=15,
            serving=4,
            link='http://example.com',
            description='Sample Description'
        )

        payload = {
            'name': 'Chicken Burger',
            'time_minutes': 10,
            'serving': 1,
            'link': 'http://burger.com',
            'description': "Mom's touch Burger i like"
        }
        url = detail_url(recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """레시피에 유저이름을 변경할 수 없다는 것을 스트"""
        new_user = create_user(
            id='new_user',
            nick_name='new_user',
            email='new@example.com'
        )
        recipe = create_recipe(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """레시피가 성공적으로 삭제되는지 테스트"""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_users_recipe_error(self):
        """다른 유저들은 해당유저의 레시피를 삭제할 수 없다는 것을 테스트"""
        new_user = create_user(
            id='new_user',
            nick_name='new_user',
            email='new@example.com'
        )
        recipe = create_recipe(user=new_user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_existing_category(self):
        """존재하는 카테고리로 레시피 생성 테스트"""
        category = Category.objects.create(name='한식')
        payload = {
            'name': 'party noodle',
            'time_minutes': 30,
            'category': category.name,
            'serving': 2,
            'link': 'http://example.com',
            'description': 'Sample Description'
        }
        res = self.client.post(RECIPE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(len(recipes), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.category.name, category.name)

    def test_create_recipe_with_invalid_category(self):
        """유효하지 않은 카테고리로 레시피 생성 테스트"""
        payload = {
            'name': 'party noodle',
            'time_minutes': 30,
            'category': '괴식',
            'serving': 2,
            'link': 'http://example.com',
            'description': 'Sample Description'
        }
        res = self.client.post(RECIPE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('category', res.data)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_recipes_includes_user_level(self):
        """레시피들을 가져올 때 유저의 칭호(level)를 가져오는지 확인"""
        # 유저의 칭호를 정의하고 레시피 생성
        level = Level.objects.create(name='Master Chef')
        self.user.level = level
        self.user.save()

        create_recipe(user=self.user, name='Spaghetti Bolognese')

        # API 요청
        res = self.client.get(RECIPE_URL)

        # 응답 데이터 확인
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('user', res.data[0])
        self.assertIn('level', res.data[0]['user'])
        self.assertEqual(res.data[0]['user']['level'], 'Master Chef')

    def test_get_recipes_by_category(self):
        """존재하는 카테고리를 가지고 있는 레시피들을 가져오는지 테스트"""
        category = Category.objects.create(name='양식')
        create_recipe(
            user=self.user,
            name='Steak',
            category=category
        )
        new_user = create_user(
            id='new_user',
            nick_name='new_user',
            email='new@example.com'
        )
        create_recipe(
            user=new_user,
            name='Cream Pasta',
            category=category
        )

        url = reverse('recipe:recipe-list-by-category', args=[category.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['category'], category.name)
        self.assertEqual(res.data[1]['category'], category.name)

    def test_get_recipes_by_nonexistent_category(self):
        """존재하지 않은 category는 검색되지 않게 테스트"""
        url = reverse('recipe:recipe-list-by-category', args=[99999])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_recipe_serializer_likes_count(self):
        """레시피에 LikeNg를 카운팅 해주는지 테스트"""
        category = Category.objects.create(name='한식')
        other_user = create_user(
            id='newuser',
            nick_name='newuser',
            email='newuser@example.com'
        )
        recipe = create_recipe(
            user=self.user,
            category=category
        )
        LikeNg.objects.create(
            rater=self.user,
            recipe_rated=recipe,
            rate=1
        )
        LikeNg.objects.create(
            rater=other_user,
            recipe_rated=recipe,
            rate=-1
        )
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = RecipeListSerializer(recipe)
        self.assertEqual(res.data[0], serializer.data)
        self.assertEqual(serializer.data['likes_count'], 1)
        self.assertEqual(serializer.data['dislikes_count'], 1)

    def test_create_recipe_with_existing_ingredient(self):
        """기존에 존재하는 재료들을 바탕으로 레시피를 만드는지 테스트"""
        # 미리 재료들을 생성
        Ingredient.objects.create(name='Lemon')
        Ingredient.objects.create(name='Fish Sauce')
        Ingredient.objects.create(name='Dragon')

        payload = {
            'name': 'party noodle',
            'time_minutes': 30,
            'serving': 2,
            'link': 'http://example.com',
            'description': 'Sample Description',
            'ingredients': [
                {'name': 'Lemon'},
                {'name': 'Fish Sauce'},
                {'name': 'Dragon'}
            ]
        }
        res = self.client.post(RECIPE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.all()
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 3)

        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(
                name=ingredient['name']
            ).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_non_existing_ingredient_error(self):
        """존재하지 않는 재료로 레시피를 만들려고 할 때 에러가 발생하는지 테스트"""
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
        res = self.client.post(RECIPE_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_update_recipe_assign_ingredient(self):
        """할당된 재료를 바탕으로 업데이트하는지 테스트"""
        # 미리 재료들을 생성
        ingredient1 = Ingredient.objects.create(name='Pepper')
        ingredient2 = Ingredient.objects.create(name='Chili')

        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient1)

        payload = {'ingredients': [{'name': 'Chili'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()  # DB에서 최신 데이터를 다시 불러옴
        self.assertIn(ingredient2, recipe.ingredients.all())
        self.assertNotIn(ingredient1, recipe.ingredients.all())

    def test_update_recipe_with_non_existing_ingredient_error(self):
        """존재하지 않는 재료로 레시피를 업데이트하려고 할 때 에러가 발생하는지 테스트"""
        ingredient = Ingredient.objects.create(name='Pepper')
        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient)

        payload = {'ingredients': [{'name': 'NonExistingIngredient'}]}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(ingredient, recipe.ingredients.all())

    def test_clear_recipe_ingredients(self):
        """레시피 재료들을 다 정리할 수 있는지 테스트"""
        ingredient = Ingredient.objects.create(name='Garlic')
        recipe = create_recipe(user=self.user)
        recipe.ingredients.add(ingredient)

        payload = {'ingredients': []}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.ingredients.count(), 0)


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
        self.category = Category.objects.create(name='한식')
        self.recipe = create_recipe(user=self.user, category=self.category)

    def tearDown(self):
        self.recipe.image.delete()

    def test_upload_image(self):
        """이미지 업로드 테스트"""
        url = image_upload_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_upload_image_to_recipe(self):
        """레시피에 이미지를 업로드하는 테스트"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                'name': 'party noodle',
                'time_minutes': 30,
                'category': self.category.name,
                'serving': 2,
                'link': 'http://example.com',
                'description': 'Sample Description',
                'image': image_file,
            }
            res = self.client.post(RECIPE_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('image', res.data)

        # Get the newly created recipe
        new_recipe = Recipe.objects.get(id=res.data['id'])
        self.assertTrue(os.path.exists(new_recipe.image.path))

    def test_update_recipe_with_image(self):
        """기존 이미지에 대해서 레시피를 업데이트하는 테스트"""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (10, 10)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {
                'name': 'party noodle',
                'time_minutes': 30,
                'category': self.category.name,
                'serving': 2,
                'link': 'http://example.com',
                'description': 'Sample Description',
                'image': image_file,
            }
            res = self.client.post(RECIPE_URL, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        url = detail_url(res.data['id'])
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            Image.new('RGB', (20, 20)).save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.patch(url, payload, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        new_recipe = Recipe.objects.get(id=res.data['id'])
        self.assertTrue(os.path.exists(new_recipe.image.path))

    def test_upload_image_bad_request(self):
        """잘못된 요청으로 이미지 업로드 테스트"""
        url = image_upload_url(self.recipe.id)
        payload = {'image': 'notimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateExtraApiTests(TestCase):
    """추가적인 API 테스트를 위한 기본 셋업 클래스"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()

        temp_image = create_temp_image()
        self.user.profile_image.save(
            'profile.jpg',
            temp_image,
            save=True
        )
        temp_image.close()

        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        """테스트 완료 후 생성된 이미지 파일 삭제"""
        if self.user.profile_image:
            self.user.profile_image.delete()


class PrivateExtraRecipeApiTests(PrivateExtraApiTests):
    """레시피 API에 대한 추가 테스트"""

    def test_get_recipe_with_profile_image(self):
        """레시피 안에 유저 프로필 이미지가 잘 반환되는지 테스트"""
        create_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = res.data[0]
        self.assertIn('profile_image', res['user'])
        self.assertTrue(os.path.exists(self.user.profile_image.path))
