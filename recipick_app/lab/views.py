"""
Views for the lab APIs.
"""
from django.http import Http404
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter
)
from drf_spectacular.types import OpenApiTypes
from django.db.models import Count

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.models import Ingredient
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

    @action(detail=False, methods=['GET'], url_path='top-lablisted')
    def top_listed_labs(self, request):
        """
        좋아요 수를 계산하여 상위 실험일지를 가져오는 메서드.
        """
        recipe_lab = Lab.objects.annotate(
            likes_count=Count('lablikes')
        ).order_by('-likes_count')[:3]

        serializer = LabListSerializer(recipe_lab, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class LabByIngredientView(generics.ListAPIView):
    """특정 재료를 포함하는 레시피를 가져오는 View"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LabListSerializer

    def list(self, request, *args, **kwargs):
        ingredient_id = self.kwargs.get('ingredient_id')

        try:
            Ingredient.objects.get(id=ingredient_id)
        except Lab.DoesNotExist:
            raise Http404('존재하지 않는 재료입니다.')

        labs = Lab.objects.filter(ingredients__id=ingredient_id)

        serializer = self.get_serializer(labs, many=True)
        return Response(serializer.data)
