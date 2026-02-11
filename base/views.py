from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from schema.base.health_check import schema_health_check

class HealthCheckView(APIView):

    permission_classes = [AllowAny]

    @schema_health_check
    def get(self, request):
        return Response({"status": "ok"})
