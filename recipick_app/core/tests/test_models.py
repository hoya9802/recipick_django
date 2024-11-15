from django.test import TestCase
from django.contrib.auth import get_user_model


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
