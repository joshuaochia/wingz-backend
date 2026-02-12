from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from schema.base.health_check import schema_health_check

from .models import Ride
from .permissions import IsAdmin
from .pagination import RidePagination
from .serializer import RideSerializer
from .filters import RideFilter


class HealthCheckView(APIView):

    permission_classes = [AllowAny]

    @schema_health_check
    def get(self, request):
        return Response({"status": "ok"})


class RideViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing rides (full CRUD).

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

    # Modular Backends
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RideFilter
    
    # Sorting Configuration
    ordering_fields = ['pickup_time', 'distance', 'created_at']
    ordering = ['-created_at']
