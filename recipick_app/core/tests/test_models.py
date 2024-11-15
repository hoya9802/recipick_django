'''from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_id_successful(self): #id로 유저를 성공적으로 생성할 수 있는지 확인

        id = 'test'
        password = 'testpass123'
        nick_name = 'abc'
        email = 'test@example.com'
        level = None
        profile_image = 'path/to/test_image.jpg'
        loc = 127 #loc를 FloatField로 정의했기 때문에 숫자로 받음

        user = get_user_model().objects.create_user(
            id=id,
            password=password,
            nick_name=nick_name,
            email=email,
            level=level,
            profile_image=profile_image,
            loc=loc
        )

        self.assertEqual(user.id, id) #생성된 사용자의 id와 우리가 제공한 id와 일치하는지 확인
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password)) #비밀번호가 맞는지 확인'''
