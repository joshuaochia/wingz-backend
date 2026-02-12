from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Ride, RideEvent

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Read Serializer for the User model - Note: if you want write, use Dj rest urls
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone_number',

        ]
        read_only_fields = ['id', 'email', 'first_name', 'last_name', 'role', 'phone_number']


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
    events = RideEventSerializer(many=True, read_only=True)
    rider = UserSerializer(source="id_rider", read_only=True)
    driver = UserSerializer(source="id_driver", read_only=True)

    class Meta:
        model = Ride
        fields = [
            'id_ride',
            'status',
            'rider',
            'driver',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
            'created_at',
            'updated_at',
            'events'
        ]
        read_only_fields = ['id_ride', 'created_at', 'updated_at', 'events']


