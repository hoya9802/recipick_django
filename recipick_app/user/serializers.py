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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'password',
            'nick_name',
            'email',
            'profile_image',
            'loc'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        # UserManager의 create_user를 사용해 유저 생성
        user = get_user_model().objects.create_user(
            id=validated_data['id'],
            email=validated_data['email'],
            password=validated_data['password'],
            # create_user 내부에서 암호화 처리
            nick_name=validated_data['nick_name']
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:  # password가 validated_data에 있을 경우
            user.set_password(password)  # 해싱하여 저장
            user.save()

        return user


class MypageSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    level = serializers.CharField(source='level.name', read_only=True)
    recipes_count = serializers.SerializerMethodField()
    labs_count = serializers.SerializerMethodField()
    freemarkets_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'profile_image',
            'level',
            'nick_name',
            'recipes_count',
            'labs_count',
            'freemarkets_count',
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

        def validate(self, data):
            if not data.get('profile_image'):
                raise serializers.ValidationError("프로필 이미지를 추가해주세요.")
            return data
