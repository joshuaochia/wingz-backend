from django.urls import path, include
from .views import HealthCheckView, RideViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')

urlpatterns = [
    path('health-check', HealthCheckView.as_view(), name="health-check"),
    path('', include(router.urls))
]