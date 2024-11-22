from django.contrib.auth import (
    get_user_model,
    authenticate,
)

from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['id', 'password', 'nick_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:  # password가 validated_data에 있을 경우
            user.set_password(password)  # 해싱하여 저장
            user.save()

        return user


class MypageSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='level.name', read_only=True)
    recipe_count = serializers.SerializerMethodField()
    labs_count = serializers.SerializerMethodField()
    freemarket_count = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
                'profile_image',
                'level',
                'nick_name',
                'recipe_count',
                'labs_count',
                'freemarket_count',
        ]

    def get_recipe_count(self, obj):
        return obj.recipe.count()

    def get_labs_count(self, obj):
        return obj.labs.count()

    def get_freemarket_count(self, obj):
        return obj.freemarket.count()


class AuthTokenSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )  # 비밀번호는 감춰지게 설정

    def validate(self, attrs):
        id = attrs.get('id')
        password = attrs.get('password')
        email = attrs.get('email')
        user = authenticate(
            request=self.context.get('request'),
            username=id,
            password=password,
            email=email,
        )  # 유효하지 않으면 None반환
        if not user:
            msg = _('제공된 정보로 인증할 수 없습니다.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
