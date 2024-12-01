from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from drf_spectacular.utils import extend_schema_field
from django.utils.translation import gettext as _

from rest_framework import serializers
from recipe.models import Recipe
from lab.models import Lab
from freemarket.models import Freemarket

from django.db.models import Count, Q


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'password',
            'password1',
            'password2',
            'nick_name',
            'email',
            'profile_image',
            'loc'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            id=validated_data['id'],
            email=validated_data['email'],
            password=validated_data['password'],
            nick_name=validated_data['nick_name']
        )
        return user

    def update(self, instance, validated_data):
        password1 = validated_data.pop('password1', None)
        password2 = validated_data.pop('password2', None)

        user = super().update(instance, validated_data)

        if password1 and password2:
            if password1 != password2:
                raise serializers.ValidationError(
                    {"password": "비밀번호가 일치하지 않습니다."}
                )
            user.set_password(password1)
            user.save()

        print(f"비밀번호 변경 완료: {user.check_password(password1)}")

        return user


class MypageSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    level = serializers.CharField(source='level.name', read_only=True)
    nick_name = serializers.CharField(read_only=True)
    recipes_count = serializers.SerializerMethodField()
    labs_count = serializers.SerializerMethodField()
    freemarkets_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    lab_likes_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'profile_image',
            'level',
            'nick_name',
            'recipes_count',
            'labs_count',
            'freemarkets_count',
            'likes_count',
            'dislikes_count',
            'lab_likes_count',
        ]

    def get_profile_image(self, obj):
        if obj.profile_image:
            return self.context['request'].build_absolute_uri(
                obj.profile_image.url
            )
        return None

    @extend_schema_field(serializers.IntegerField)
    def get_recipes_count(self, obj):
        return Recipe.objects.filter(user=obj).count()

    @extend_schema_field(serializers.IntegerField)
    def get_labs_count(self, obj):
        return Lab.objects.filter(user=obj).count()

    @extend_schema_field(serializers.IntegerField)
    def get_freemarkets_count(self, obj):
        return Freemarket.objects.filter(user=obj).count()

    @extend_schema_field(serializers.IntegerField)
    def get_likes_count(self, obj):
        return Recipe.objects.filter(user=obj).aggregate(
            total_likes=Count('likes', filter=Q(likes__rate=1))
        )['total_likes'] or 0

    @extend_schema_field(serializers.IntegerField)
    def get_dislikes_count(self, obj):
        return Recipe.objects.filter(user=obj).aggregate(
            total_dislikes=Count('likes', filter=Q(likes__rate=-1))
        )['total_dislikes'] or 0

    @extend_schema_field(serializers.IntegerField)
    def get_lab_likes_count(self, obj):
        return Lab.objects.filter(user=obj).aggregate(
            total_likes=Count('lablikes')
        )['total_likes'] or 0


class AuthTokenSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )  # 비밀번호는 감춰지게 설정

    def validate(self, attrs):
        id = attrs.get('id')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=id,
            password=password,
        )  # 유효하지 않으면 None반환
        if not user:
            msg = _('제공된 정보로 인증할 수 없습니다.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ProfileImageSerializer(serializers.ModelSerializer):
    """프로필 이미지 업로드를 위한 serializer"""

    class Meta:
        model = get_user_model()
        fields = ['profile_image']

        def validate(self, attrs):
            if not attrs.get('profile_image'):
                raise serializers.ValidationError("프로필 이미지를 추가해주세요.")
            return attrs
