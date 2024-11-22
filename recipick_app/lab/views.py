"""
Views for the lab APIs.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter
)
from drf_spectacular.types import OpenApiTypes

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from lab.models import Lab, Like
from .serializers import (
    LabSerializer,
    LabListSerializer,
    LabImageSerializer,
    LikeSerializer,
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'all',
                OpenApiTypes.STR, enum=['true', 'false'],
                description='Retrieve all labs if true.',
            )
        ]
    )
)
class LabViewSet(viewsets.ModelViewSet):
    """Lab APIs을 관리하기 위한 ViewSet"""
    serializer_class = LabSerializer
    queryset = Lab.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        인증한 유저의 실험일지들도 가져온다.
        url 뒤에 쿼리문이 True이면 모든 유저들의 실험일지를 가져온다.
        """
        if self.action == 'retrieve':
            return self.queryset

        all_labs = self.request.query_params.get('all')

        if all_labs == 'true':
            return Lab.objects.all().order_by('-modify_dt')
        return Lab.objects.filter(
            user=self.request.user
        ).order_by('-modify_dt')

    def get_serializer_class(self):
        """요청에 따라서 다른 Serializer을 사용하기 위한 메서드"""
        if self.action == 'list':
            return LabListSerializer
        elif self.action == 'upload_image':
            return LabImageSerializer

        return LabSerializer

    def perform_create(self, serializer):
        """새로운 실험일지를 만드는 메서드"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """레시피에 이미지를 업로드하는 메서드"""
        lab = self.get_object()
        serializer = self.get_serializer(lab, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeViewSet(viewsets.ModelViewSet):
    """Like을 관리하기 위한 ViewSet"""
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        lab_id = request.data.get('exlog')

        try:
            like = Like.objects.get(
                user=user,
                exlog_id=lab_id
            )
            if like:
                like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        except Like.DoesNotExist:
            like = Like.objects.create(
                user=user,
                exlog_id=lab_id,
            )
            serializer = self.get_serializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
