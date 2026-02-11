from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

schema_health_check = extend_schema(
    summary="Health Check",
    description="Health check for server",
    auth=None,
    responses={
        200: inline_serializer(
            name='HealthCheckResponse',
            fields={
                'status': serializers.CharField(default='ok')
            }
        )
    }
)