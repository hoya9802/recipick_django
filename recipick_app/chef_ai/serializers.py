from rest_framework import serializers


class InputDataSerializer(serializers.Serializer):
    ingredients = serializers.ListField(
        child=serializers.CharField(max_length=10)
    )
