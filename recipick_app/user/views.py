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
            methods=['GET', 'PUT', 'PATCH', 'DELETE'],
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

        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

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
