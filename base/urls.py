from django.urls import path, include
from .views import HealthCheckView, RideViewSet, UserViewSet, RideEventsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'ride-events', RideEventsViewSet, basename='ride-events')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('health-check', HealthCheckView.as_view(), name="health-check"),
    path('', include(router.urls))
]