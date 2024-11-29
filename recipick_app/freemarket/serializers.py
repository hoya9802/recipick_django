"""
Serializers for freemarket APIs.
"""
from django.utils import timezone

from rest_framework import serializers

from recipe.serializers import (
    NicknameSerializer,
    RecipeImageSerializer
)

from freemarket.models import Freemarket


class FreemarketListSerializer(serializers.ModelSerializer):
    """자유시장 List view을 위한 serializer"""
    user = NicknameSerializer(read_only=True)
    days_ago = serializers.SerializerMethodField()

    class Meta:
        model = Freemarket
        fields = [
            'id',
            'user',
            'name',
            'image',
            'is_shared',
            'days_ago',
        ]
        read_only_fields = ['id']

    def get_days_ago(self, obj):
        """현재 날짜와 수정일자의 차이를 계산하고 return"""
        today = timezone.localdate()
        diff_days = (today-obj.modify_dt).days

        if diff_days == 0:
            return "오늘"
        elif diff_days == 1:
            return "하루 전"
        else:
            return f'{diff_days}일 전'


class FreemarketSerializer(FreemarketListSerializer):
    class Meta(FreemarketListSerializer.Meta):
        fields = FreemarketListSerializer.Meta.fields + [
            'count',
            'purchase_dt',
            'description',
        ]


class FreemarketImageSerializer(RecipeImageSerializer):
    """자유시장 이미지 업로드를 위한 Serializer"""
    class Meta(RecipeImageSerializer.Meta):
        model = Freemarket
        fields = RecipeImageSerializer.Meta.fields
