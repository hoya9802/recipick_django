from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
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

    def test_users_lists(self):
        # 사용자 목록이 올바르게 표시되는지 확인
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.id)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        # 사용자 수정페이지가 열리는지 확인
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        # 사용자 생성페이지가 열리는지 확인
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
