"""
Views for the recipe APIs.
"""
from django.http import Http404
from django.db.models import Count, Q, F

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter
)
from drf_spectacular.types import OpenApiTypes

from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.models import Recipe, Category, LikeNg, Ingredient
from .serializers import (
    RecipeSerializer,
    RecipeListSerializer,
    CategorySerializer,
    LikeNgSerializer,
    RecipeImageSerializer,
    IngredientSerializer,
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
        if self.action == 'retrieve':
            return self.queryset

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
        elif self.action == 'upload_image':
            return RecipeImageSerializer

        return RecipeSerializer

    def perform_create(self, serializer):
        """새로운 레시피를 만드는 메서드"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """레시피에 이미지를 업로드하는 메서드"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='top-ranked')
    def top_ranked_recipes(self, request):
        """
        좋아요 수와 NG 수를 합산하여 상위 레시피를 가져오는 메서드.
        """
        top_recipes = Recipe.objects.annotate(
            likes_count=Count('likes', filter=Q(likes__rate=1)),
            ng_count=Count('likes', filter=Q(likes__rate=-1)),
            score=F('likes_count') - F('ng_count')  # 좋아요 - NG로 점수 계산
        ).filter(score__gt=0)  # score가 0보다 큰 레시피만 가져옴
        top_recipes = top_recipes.order_by('-score', '-likes_count')[:5]

        serializer = RecipeListSerializer(top_recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='top-nglisted')
    def top_nglisted_recipes(self, request):
        """
        NG 수를 계산하여 상위 레시피를 가져오는 메서드.
        """
        ng_recipes = Recipe.objects.annotate(
            ng_count=Count('likes', filter=Q(likes__rate=-1))
        ).order_by('-ng_count')[:5]

        serializer = RecipeListSerializer(ng_recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            like_ng = LikeNg.objects.get(
                rater=rater,
                recipe_rated_id=recipe_id
            )
            if like_ng.rate == int(rate):
                like_ng.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                like_ng.rate = int(rate)
                like_ng.save()
                serializer = self.get_serializer(like_ng)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except LikeNg.DoesNotExist:
            like_ng = LikeNg.objects.create(
                rater=rater,
                recipe_rated_id=recipe_id,
                rate=rate
            )
            serializer = self.get_serializer(like_ng)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'], url_path='user-liked')
    def user_liked_recipes(self, request):
        """
        사용자가 좋아요한 레시피를 반환하는 메서드.
        """
        liked_recipes = Recipe.objects.filter(
            likes__rater=request.user,
            likes__rate=1
        ).distinct()
        serializer = RecipeListSerializer(liked_recipes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], url_path='user-disliked')
    def user_disliked_recipes(self, request):
        """
        사용자가 싫어요한 레시피를 반환하는 메서드.
        """
        disliked_recipes = Recipe.objects.filter(
            likes__rater=request.user,
            likes__rate=-1
        ).distinct()
        serializer = RecipeListSerializer(disliked_recipes, many=True)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """db에서 재료들을 관리하기 위한 ViewSet"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by('name')
