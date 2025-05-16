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

import requests
import os


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
        print("serializer: ", serializer)
        if serializer.is_valid():
            input_data = serializer.validated_data
            print("input_data: ", input_data)
            try:
                headers = {
                    "Authorization": (
                        f"Bearer {os.environ.get('RUNPOD_API_KEY')}"
                    ),
                    "Content-Type": "application/json"
                }
                response = requests.post(
                    os.environ.get('RUNPOD_API_URL'),
                    headers=headers,
                    json=input_data
                )
                response.raise_for_status()
                return Response(response.json(), status=status.HTTP_200_OK)
            except requests.RequestException as e:
                return Response(
                    {"error": f"AI 서비스 연결 오류: {str(e)}"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
