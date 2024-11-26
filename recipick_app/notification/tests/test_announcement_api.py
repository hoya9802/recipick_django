"""
Announcement API 테스트
"""
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.tests.test_recipe_api import create_user

from notification.models import Announcement
from notification.serializers import (
    AnnouncementSerializer,
    AnnouncementListSerializer
)


ANNOUNCEMENTS_URL = reverse('notification:announcement-list')


def detail_url(announcement_id):
    """Announcement detail URL을 생성하고 반환"""
    return reverse('notification:announcement-detail', args=[announcement_id])


class PublicAnnouncementsApiTests(TestCase):
    """인증받지 못한 사람에 대한 테스트"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """재료를 가져올때 오류를 발생시키는지 테스트"""
        res = self.client.get(ANNOUNCEMENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAnnouncementsApiTests(TestCase):
    """인증받은 유저에 대한 API요청 테스트"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_announcement(self):
        """공지사항들을 잘 가져오는지 테스트"""
        Announcement.objects.create(
            title='삼겹살',
            contents='삼겹살 공지사항'
        )
        Announcement.objects.create(
            title='참치',
            contents='참치 공지사항'
        )

        res = self.client.get(ANNOUNCEMENTS_URL)

        announcements = Announcement.objects.all().order_by('-announce_dt')
        serializer = AnnouncementListSerializer(announcements, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_announcement_detail(self):
        """공지사항의 디테일 정보를 잘 가져오는지 테스트"""
        announcement = Announcement.objects.create(
            title='삼겹살',
            contents='삼겹살 공지사항'
        )

        url = detail_url(announcement.id)
        res = self.client.get(url)

        serializer = AnnouncementSerializer(announcement)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
