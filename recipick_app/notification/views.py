from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from notification.models import Announcement, Expiration
from .serializers import (
    AnnouncementSerializer,
    AnnouncementListSerializer,
    ExpirationSerializer,
    ExpirationListSerializer,
    ExpirationImageSerializer,
)


class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    """db에서 공지사항들을 관리하기 위한 ViewSet"""
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by('-announce_dt')

    def get_serializer_class(self):
        """요청에 따라서 다른 Serializer을 사용하기 위한 메서드"""
        if self.action == 'list':
            return AnnouncementListSerializer

        return AnnouncementSerializer


class ExpirationViewSet(viewsets.ReadOnlyModelViewSet):
    """db에서 유통기한 공지사항들을 관리하기 위한 ViewSet"""
    serializer_class = ExpirationSerializer
    queryset = Expiration.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by('title')

    def get_serializer_class(self):
        """요청에 따라서 다른 Serializer을 사용하기 위한 메서드"""
        if self.action == 'list':
            return ExpirationListSerializer
        elif self.action == 'upload_image':
            return ExpirationImageSerializer

        return ExpirationSerializer
