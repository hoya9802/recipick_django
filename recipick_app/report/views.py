from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from .serializers import ReportpageSerializer
from .models import Reportpage


class ReportpageView(APIView):
    serializer_class = ReportpageSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        reports = Reportpage.objects.all()
        serializer = self.serializer_class(reports, many=True)
        return Response(serializer.data)
