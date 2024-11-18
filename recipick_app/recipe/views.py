"""
Views for the recipe APIs.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter
)
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.models import Recipe, Category
from .serializers import (
    RecipeSerializer,
    RecipeListSerializer,
    CategorySerializer,
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
    """Recipe APIs을 관리하기 위한 View"""
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
