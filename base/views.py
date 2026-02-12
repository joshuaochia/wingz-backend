from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from schema.base.health_check import schema_health_check

from .models import Ride
from .permissions import IsAdmin
from .pagination import RidePagination
from .serializer import RideSerializer


class HealthCheckView(APIView):

    permission_classes = [AllowAny]

    @schema_health_check
    def get(self, request):
        return Response({"status": "ok"})


class RideViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing rides (full CRUD).
    
    Provides:
    - list: GET /api/rides/
    - retrieve: GET /api/rides/{id_ride}/
    - create: POST /api/rides/
    - update: PUT /api/rides/{id_ride}/
    - partial_update: PATCH /api/rides/{id_ride}/
    - delete: DELETE /api/rides/{id_ride}/
    
    Features:
    - Nested RideEvents and Users (id_rider, id_driver)
    - Pagination support
    - Optimized database queries
    - Admin-only access
    """
    queryset = Ride.objects.select_related(
        'id_rider',
        'id_driver'
    ).prefetch_related(
        'events'
    ).order_by('-created_at')
    
    serializer_class = RideSerializer
    permission_classes = [IsAdmin]
    pagination_class = RidePagination
    lookup_field = 'id_ride'