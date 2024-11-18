from rest_framework import serializers
from report.models import Reportpage


class ReportpageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reportpage
        fields = [
            'reporter',
            'link',
            'create_dt',
            'detail',
        ]
