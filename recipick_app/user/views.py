from rest_framework import (
    generics,
    authentication,
    permissions,
    status,
    viewsets,
)

from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from core.models import User
from rest_framework.decorators import action
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    MypageSerializer,
    ProfileImageSerializer
)
# gmail api
import json
from rest_framework.viewsets import ViewSet
from .gmail import send_email
import random
import string
from django.contrib.auth.hashers import make_password


class AccountViewSet(ViewSet):
    @action(detail=False, methods=['post'])
    def find_id(self, request):
        token_path = 'user/secrets/token.json'

        # Step 1: token.json 파일 읽기
        try:
            with open(token_path, 'r') as token_file:
                json.load(token_file)
        except FileNotFoundError:
            return Response(
                {"error": "token.json 파일을 찾을 수 없습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except json.JSONDecodeError:
            return Response(
                {"error": "token.json 파일을 파싱할 수 없습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Step 2: 이메일 입력 확인
        email = request.data.get('email')
        if not email:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Step 3: 이메일로 유저 확인 및 이메일 전송
        try:
            user = User.objects.get(email=email)
            send_email(
                to_email=email,
                subject="Recipick - Id",
                body=f"아이디는 {user.id} 입니다.",
            )
            return Response(
                {"message": f"아이디를 {email}로 전송했습니다."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": "입력하신 이메일로 가입된 아이디는 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def reset_password(self, request):
        # Step 1: 이메일 입력 확인
        email = request.data.get('email')
        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Step 2: 사용자 확인
            user = User.objects.get(email=email)

            # Step 3: 임시 비밀번호 생성
            temporary_password = ''.join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )

            # Step 4: 비밀번호 암호화 후 저장
            user.password = make_password(temporary_password)
            user.save()

            # Step 5: 이메일로 임시 비밀번호 전송 (Gmail API 사용)
            send_email(
                to_email=email,
                subject="Recipick - Password",
                body=(
                    f"임시 비밀번호는 {temporary_password} 입니다.\n"
                    "로그인 후 반드시 비밀번호를 수정해주세요."
                ),
            )

            return Response(
                {"message": f"임시 비밀번호를 {email}로 전송하였습니다."},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"error": "입력하신 이메일로 가입된 계정이 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """적합한 시리얼라이저 반환"""
        if self.action == 'profile':
            return ProfileImageSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    @action(detail=False,
            methods=['GET', 'PUT', 'PATCH'],
            url_path='me', name='me')
    def me(self, request):
        """현재 사용자 정보 반환 및 수정/삭제"""
        user = self.get_object()

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=(request.method == 'PATCH')
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=['POST'],
        url_path='delete',
        name='delete'
    )
    def delete(self, request):
        """비밀번호 확인 후 회원 탈퇴"""
        user = self.get_object()
        password = request.data.get('password')

        # 비밀번호가 제공되지 않았을 경우
        if not password:
            return Response(
                {"error": "비밀번호를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호 검증
        if not user.check_password(password):
            return Response(
                {"error": "비밀번호가 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호가 일치하면 계정 삭제
        user.delete()
        return Response(
            {"message": "회원 탈퇴가 완료되었습니다."},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(methods=['POST'],
            detail=False,
            url_path='profile', url_name='profile')
    def profile(self, request):
        """프로필 이미지를 업로드하는 메서드"""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MypageView(APIView):
    serializer_class = MypageSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user, context={'request': request})
        return Response(serializer.data)
