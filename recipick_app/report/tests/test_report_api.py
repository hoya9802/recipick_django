from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


REPORT_URL = reverse('report:reportview')


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class AdminReportPageTests(TestCase):

    def setUp(self):
        self.admin = create_superuser(
            id='admin',
            password='admin123',
            email='admin@example.com',
        )

        self.user = create_user(
            id='test',
            password='test123',
            nick_name='test123',
            email='test@example.com',
        )

        self.client = APIClient()

    def test_report_admin_success(self):
    # 관리자가 신고페이지를 조회 할 수 있는지 확인
        self.client.force_authenticate(user=self.admin)
        res = self.client.get(REPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_report_user_error(self):
    # 유저가 신고페이지에 조회 할 수 없는지 확인
        self.client.force_authenticate(user=self.user)
        res = self.client.get(REPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
