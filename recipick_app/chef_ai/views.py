from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample
)

from .serializers import InputDataSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .main import generate_recipe


@extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'ingredients': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'example': ['mushroom', 'cabbage', 'soy sauce']
                }
            }
        }
    },
    responses={200: None},
    examples=[
        OpenApiExample(
            'Valid Example',
            value={'ingredients': ['mushroom', 'cabbage', 'soy sauce']},
            request_only=True
        )
    ]
)
class AiChefAPIView(APIView):
    """AI chef에게 음식을 추천받기 위한 ViewSet"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = InputDataSerializer(data=request.data)

        if serializer.is_valid():
            input_data = serializer.validated_data['ingredients']
            response = generate_recipe(input_data)

            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
