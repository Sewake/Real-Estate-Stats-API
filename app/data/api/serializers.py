from rest_framework import serializers


class ChargesStatsQuerySerializer(serializers.Serializer):
    department_code = serializers.CharField(required=False, max_length=3)
    city = serializers.CharField(required=False, max_length=128)
    postal_code = serializers.CharField(required=False, max_length=10)

    def validate(self, attrs):
        if not (
            attrs.get("department_code")
            or attrs.get("city")
            or attrs.get("postal_code")
        ):
            raise serializers.ValidationError(
                "Provide at least one filter: department_code, city or postal_code."
            )
        return attrs


class BieniciImportSerializer(serializers.Serializer):
    url = serializers.URLField()
