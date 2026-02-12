from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    Inherits from AbstractUser which includes:
    - id, username, first_name, last_name, email, password
    """
    
    # Role choices
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('driver', 'Driver'),
        ('rider', 'Rider'),
    ]

    # Override email to make it unique, required, and indexed
    email = models.EmailField(
        unique=True, 
        db_index=True,
        help_text="User's unique email address"
    )

    # Additional fields not in AbstractUser
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='rider',
        help_text="User's role in the system"
    )
    
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="User's phone number"
    )

    @property
    def id_user(self):
        """Alias for compatibility with your naming convention"""
        return self.id

    class Meta:
        # Adding explicit indexes for the Meta class as well
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]

class Ride(models.Model):
    """
    Ride model for the Wingz ride-sharing application.
    Tracks ride information including status, participants, and location details.
    """
    
    # Status choices
    STATUS_CHOICES = [
        ('en-route', 'En Route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Primary key
    id_ride = models.AutoField(primary_key=True)
    
    # Ride status
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='requested',
        help_text="Current status of the ride"
    )
    
    # Foreign keys to User model
    id_rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rides_as_rider',
        help_text="User who requested the ride"
    )
    
    id_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rides_as_driver',
        help_text="Driver assigned to the ride"
    )
    
    # Pickup location
    pickup_latitude = models.FloatField(
        help_text="Latitude coordinate of pickup location"
    )
    
    pickup_longitude = models.FloatField(
        help_text="Longitude coordinate of pickup location"
    )
    
    # Dropoff location
    dropoff_latitude = models.FloatField(
        help_text="Latitude coordinate of dropoff location"
    )
    
    dropoff_longitude = models.FloatField(
        help_text="Longitude coordinate of dropoff location"
    )
    
    # Pickup time
    pickup_time = models.DateTimeField(
        help_text="Scheduled or actual pickup time"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ride'
        ordering = ['-pickup_time']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['pickup_time']),
            models.Index(fields=['id_rider']),
            models.Index(fields=['id_driver']),
        ]


class RideEvent(models.Model):
    """
    RideEvent model for tracking events that occur during a ride.
    Examples: ride requested, driver assigned, driver arrived, 
    ride started, ride completed, etc.
    """
    
    # Primary key
    id_ride_event = models.AutoField(primary_key=True)
    
    # Foreign key to Ride
    id_ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name='events',
        help_text="Ride associated with this event"
    )
    
    # Event description
    description = models.CharField(
        max_length=255,
        help_text="Description of what happened in this event"
    )
    
    # Timestamp of when the event occurred
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp of when the event occurred"
    )
