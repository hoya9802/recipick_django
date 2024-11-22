from rest_framework import serializers

from freemarket.serializers import RecipeImageSerializer
from .models import Announcement, Expiration


class ExpirationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expiration
        fields = ['id', 'title', 'image']
        read_only_fields = ['id']


class ExpirationSerializer(ExpirationListSerializer):
    class Meta(ExpirationListSerializer.Meta):
        fields = ExpirationListSerializer.Meta.fields + [
            'description',
            'url'
        ]


class ExpirationImageSerializer(RecipeImageSerializer):
    """유통기한 이미지 업로드를 위한 Serializer"""
    class Meta(RecipeImageSerializer.Meta):
        model = Expiration
        fields = RecipeImageSerializer.Meta.fields


class AnnouncementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'announce_dt']
        read_only_fields = ['id']


class AnnouncementSerializer(AnnouncementListSerializer):
    class Meta(AnnouncementListSerializer.Meta):
        fields = AnnouncementListSerializer.Meta.fields + [
            'contents'
        ]
