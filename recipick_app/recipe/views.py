"""
Views for the recipe APIs.
"""
from django.http import Http404

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter
)
from drf_spectacular.types import OpenApiTypes

from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.models import Recipe, Category, LikeNg
from .serializers import (
    RecipeSerializer,
    RecipeListSerializer,
    CategorySerializer,
    LikeNgSerializer
)


class CategoryListView(generics.ListAPIView):
    """Category APIs을 관리하기 위한 view"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'all',
                OpenApiTypes.STR, enum=['true', 'false'],
                description='Retrieve all recipes if true.',
            )
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """Recipe APIs을 관리하기 위한 ViewSet"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        인증한 유저의 레시피들도 가져온다.
        url 뒤에 쿼리문이 True이면 모든 유저들의 레시피를 가져온다.
        """
        all_recipes = self.request.query_params.get('all')

        if all_recipes == 'true':
            return Recipe.objects.all().order_by('-modify_dt')
        return Recipe.objects.filter(
            user=self.request.user
        ).order_by('-modify_dt')

    def get_serializer_class(self):
        """요청에 따라서 다른 Serializer을 사용하기 위한 메서드"""
        if self.action == 'list':
            return RecipeListSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        """새로운 레시피를 만드는 메서드"""
        serializer.save(user=self.request.user)


class RecipesByCategoryListView(generics.ListAPIView):
    """카테코리에 맞는 레시피들을 가져오는 ListView"""
    serializer_class = RecipeListSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', 99999)
        if not Category.objects.filter(id=category_id).exists():
            raise Http404('존재하지 않은 카테고리입니다.')
        return Recipe.objects.filter(category_id=category_id)


class LikeNgViewSet(viewsets.ModelViewSet):
    """LikeNg을 관리하기 위한 ViewSet"""
    serializer_class = LikeNgSerializer
    queryset = LikeNg.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        rater = request.user
        recipe_id = request.data.get('recipe_rated')
        rate = request.data.get('rate')

        try:
            like_ng = LikeNg.objects.get(rater=rater, recipe_rated_id=recipe_id)
            if like_ng.rate == int(rate):
                like_ng.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                like_ng.rate = int(rate)
                like_ng.save()
                serializer = self.get_serializer(like_ng)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except LikeNg.DoesNotExist:
            like_ng = LikeNg.objects.create(rater=rater, recipe_rated_id=recipe_id, rate=rate)
            serializer = self.get_serializer(like_ng)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
