from rest_framework import serializers
from report.models import Report, Status


class ReportSerializer(serializers.ModelSerializer):
    status = serializers.StringRelatedField()

    class Meta:
        model = Report
        fields = [
            'reporter',
            'reported_user',
            'url',
            'detail',
            'status',
            'create_dt',
        ]
        read_only_fields = ['reporter', 'status']

    def create(self, validated_data):
        validated_data['reporter'] = self.context['request'].user
        validated_data['status'] = Status.objects.get(status='접수완료')
        report = super().create(validated_data)
        return report
