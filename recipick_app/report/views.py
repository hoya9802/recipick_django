from rest_framework import status, authentication, permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ReportSerializer
from .models import Report


class ReportView(APIView):
    serializer_class = ReportSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_staff:
            return Response({'detail': '접근 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        reports = Report.objects.all()
        serializer = self.serializer_class(reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
