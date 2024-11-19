from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from recipe.models import Recipe
from report.models import Report, Status

REPORT_URL = reverse('report:report-list')


def create_superuser(**params):
    return get_user_model().objects.create_superuser(**params)


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def create_recipe(**params):
    return Recipe.objects.create(**params)


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
        # 유저가 신고페이지를 조회 할 수 없는지 확인
        self.client.force_authenticate(user=self.user)
        res = self.client.get(REPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class ReportTests(TestCase):

    def setUp(self):
        Status.objects.create(status='접수완료')
        self.user1 = create_user(
            id='user1',
            password='user123',
            nick_name='user12',
            email='user1@example.com',
        )
        self.user2 = create_user(
            id='user2',
            password='user1234',
            nick_name='user123',
            email='user2@example.com',
        )

        self.client = APIClient()

    def test_user_recipe_reportcreate_success(self):
        # 유저가 레시피를 신고 할 수 있는지 확인
        self.client.force_authenticate(user=self.user1)
        payload = {
            'reported_user': self.user2.id,
            'url': 'http://recipick.com/recipe',
            'detail': '불쾌한 이미지와 설명',
        }

        res = self.client.post(REPORT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('detail', res.data)

        report = Report.objects.filter(
                    reporter=self.user1,
                    url=payload['url']).first()

        self.assertIsNotNone(report)
        self.assertEqual(report.reporter, self.user1)
        self.assertEqual(report.url, payload['url'])
        self.assertEqual(report.detail, payload['detail'])
