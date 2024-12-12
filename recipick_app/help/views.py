"""
Views for the help APIs.
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

from help.models import Help, Comment
from .serializers import (
    HelpSerializer,
    HelpListSerializer,
    HelpImageSerializer,
    CommentSerializer
)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'all',
                OpenApiTypes.STR, enum=['true', 'false'],
                description='Retrieve all Helps if true.',
            )
        ]
    )
)
class HelpViewSet(viewsets.ModelViewSet):
    """지식인 APIs을 관리하기 위한 ViewSet"""
    serializer_class = HelpSerializer
    queryset = Help.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        인증한 유저의 지식인글을 가져온다.
        url 뒤에 쿼리문이 True이면 모든 유저들의 지식인글을 가져온다.
        """
        if self.action == 'retrieve':
            return self.queryset

        all_helps = self.request.query_params.get('all')

        if all_helps == 'true':
            return Help.objects.all().order_by('-modify_dt')
        return Help.objects.filter(
            user=self.request.user
        ).order_by('-modify_dt')

    def get_serializer_class(self):
        """요청에 따라서 다른 Serializer을 사용하기 위한 메서드"""
        if self.action == 'list':
            return HelpListSerializer
        elif self.action == 'upload_image':
            return HelpImageSerializer

        return HelpSerializer

    def perform_create(self, serializer):
        """새로운 지식인을 만드는 메서드"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """지식인에 이미지를 업로드하는 메서드"""
        help = self.get_object()
        serializer = self.get_serializer(help, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            post_id = self.request.query_params.get('post')
            if post_id:
                return self.queryset.filter(
                    post_id=post_id).order_by('-create_dt')
            return self.queryset.none()
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            comment = self.get_object()
        except Exception:
            return Response(
                {'error': '댓글이 없음'},
                status=status.HTTP_404_NOT_FOUND
            )

        if comment.user != request.user:
            return Response(
                {'error': '내가 작성한 댓글이 아닙니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(
                        comment,
                        data=request.data,
                        partial=True
                    )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        print(f"Deleting comment with ID: {pk}")  # 요청된 ID 출력
        try:
            comment = self.get_object()
            print(f"Found comment: {comment}")
        except Exception as e:
            print(f"Error finding comment: {e}")
            return Response(
                {'error': '댓글이 없음'},
                status=status.HTTP_404_NOT_FOUND
            )

        if comment.user != request.user:
            return Response(
                {'error': '내가 작성한 댓글이 아닙니다.'},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)
