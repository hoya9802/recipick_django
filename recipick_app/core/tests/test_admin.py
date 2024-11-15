from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):

    def setUp(self): #각 테스트 메서드 실행되기 전에 자동으로 호출됨
        self.client = Client() #테스트를 진행할 수 있게 하는 Client() 초기화
        self.admin_user = get_user_model().objects.create_superuser(
            id='admin',
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            id='testuser',
            email='user@example.com',
            password='testpass123',
            nick_name='user_nick'
        )

    def test_users_lists(self): #사용자 목록이 올바르게 표시되는지 확인
        url = reverse('admin:core_user_changelist') #장고에서 어떤 url을 가져올지 결정
        res = self.client.get(url)

        self.assertContains(res, self.user.id)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self): #사용자 수정페이지가 열리는지 확인
        url = reverse('admin:core_user_change', args=[self.user.id]) #self.user의 id를 url에 전달하여 페이지 생성
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self): #사용자 생성페이지가 열리는지 확인
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
