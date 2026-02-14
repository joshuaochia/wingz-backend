from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Ride, RideEvent
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Read Serializer for the User model - Note: if you want write, use Dj rest urls
    """
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'role',
            'phone_number',
            'first_name',
            'last_name'
        ]
        read_only_fields = ['id', 'email', 'role', 'phone_number', 'first_name', 'last_name']


class RideEventSerializer(serializers.ModelSerializer):
    """
    Serializer for the RideEvent model.
    """
    class Meta:
        model = RideEvent
        fields = [
            'id_ride_event',
            'id_ride',
            'description',
            'created_at',
        ]
        read_only_fields = ['id_ride_event', 'created_at']


class RideSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ride model.
    """

    todays_ride_events = serializers.SerializerMethodField()
    rider = UserSerializer(source="id_rider", read_only=True)
    driver = UserSerializer(source="id_driver", read_only=True)

    class Meta:
        model = Ride
        fields = [
            'id_ride',
            "driver",
            "rider",
            'status',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
            'created_at',
            'updated_at',
            'todays_ride_events',
        ]

    def get_todays_ride_events(self, obj):
        if hasattr(obj, 'todays_events'):
            return RideEventSerializer(obj.todays_events, many=True).data
        
        # Fallback for when serializer is used outside ViewSet context
        events = obj.events.filter(
            created_at__gte=timezone.now() - timedelta(days=1)
        )
        return RideEventSerializer(events, many=True).data