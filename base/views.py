from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Prefetch
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

from schema.base.health_check import schema_health_check

from .models import Ride, RideEvent
from .permissions import IsAdmin
from .pagination import RidePagination, BasePagination
from .serializers import RideSerializer, RideEventSerializer, UserSerializer
from .filters import RideFilter

User = get_user_model()

class HealthCheckView(APIView):
    """
    Health check API for server services.
    """
    permission_classes = [AllowAny]

    @schema_health_check
    def get(self, request):
        return Response({"status": "ok"})


class UserViewSet(viewsets.ModelViewSet):

    """
    ViewSet for managing U sers (full CRUD).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = BasePagination


class RideEventsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Ride events (full CRUD).
    """
    queryset = RideEvent.objects.all().order_by('-created_at')
    serializer_class = RideEventSerializer
    permission_classes = [IsAdmin]
    pagination_class = BasePagination


class RideViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing rides (full CRUD).

    Features:
    - Nested RideEvents and Users (id_rider, id_driver)
    - Pagination support
    - Optimized database queries
    - Admin-only access
    - Sorting & Filtering
    """
    queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related(
        Prefetch(
            'events',
            queryset=RideEvent.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=1)
            ),
            to_attr='todays_events'
        )
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
