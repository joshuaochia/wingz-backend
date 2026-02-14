import pytest
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from base.models import Ride, RideEvent

User = get_user_model()

@pytest.fixture
def sample_ride(rider, driver):
    return Ride.objects.create(
        id_rider=rider,
        id_driver=driver,
        status='pending',
        pickup_latitude=37.7749,
        pickup_longitude=-122.4194,
        dropoff_latitude=37.7849,
        dropoff_longitude=-122.4094,
        pickup_time=timezone.now() + timedelta(hours=1)
    )

# CUSTOM BUSINESS LOGIC TESTS ONLY

@pytest.mark.django_db
class TestTodaysEventsFiltering:
    """Test custom 24-hour filtering logic."""
    
    def test_only_last_24_hours_events_returned(self, authenticated_client, sample_ride):
        """Only events from last 24 hours are included."""
        now = timezone.now()
        
        # Create events normally
        recent = RideEvent.objects.create(
            id_ride=sample_ride,
            description="Recent event"
        )
        hours_ago = RideEvent.objects.create(
            id_ride=sample_ride,
            description="23 hours ago"
        )
        old = RideEvent.objects.create(
            id_ride=sample_ride,
            description="Old event"
        )
        
        # Update timestamps (bypasses auto_now_add)
        RideEvent.objects.filter(id_ride_event=hours_ago.id_ride_event).update(
            created_at=now - timedelta(hours=23)
        )
        RideEvent.objects.filter(id_ride_event=old.id_ride_event).update(
            created_at=now - timedelta(days=2)
        )
        
        response = authenticated_client.get(f'/api/base/rides/{sample_ride.id_ride}/')
        event_data = response.data['todays_ride_events']
        
        # Your custom logic: only last 24 hours
        assert len(event_data) == 2
        descriptions = [e['description'] for e in event_data]
        assert "Old event" not in descriptions
        assert "Recent event" in descriptions
        assert "23 hours ago" in descriptions


@pytest.mark.django_db
class TestDistanceCoordinateValidation:
    """Test YOUR custom coordinate validation logic."""
    
    def test_partial_coordinates_rejected(self, authenticated_client, sample_ride):
        """YOUR validation: both lat and lng required together."""
        response = authenticated_client.get('/api/base/rides/?lat=37.7749')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'coordinates' in response.data
        
        response = authenticated_client.get('/api/base/rides/?lng=-122.4194')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_invalid_coordinate_format_rejected(self, authenticated_client, sample_ride):
        """YOUR validation: coordinates must be numeric."""
        response = authenticated_client.get('/api/base/rides/?lat=abc&lng=-122.4194')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_coordinate_range_validation(self, authenticated_client, sample_ride):
        """YOUR validation: lat -90 to 90, lng -180 to 180."""
        # Invalid latitude
        response = authenticated_client.get('/api/base/rides/?lat=91&lng=-122.4194')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Invalid longitude
        response = authenticated_client.get('/api/base/rides/?lat=37.7749&lng=181')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Valid should pass
        response = authenticated_client.get('/api/base/rides/?lat=37.7749&lng=-122.4194')
        assert response.status_code == status.HTTP_200_OK
    