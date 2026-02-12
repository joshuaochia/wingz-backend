from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q
from base.models import Ride, RideEvent

User = get_user_model()

class Command(BaseCommand):
    help = 'Clears all Rides, RideEvents, and non-admin Users'

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing data...")
        
        # 1. Delete RideEvents first (Child)
        events_count = RideEvent.objects.all().delete()[0]
        
        # 2. Delete Rides (Parent)
        rides_count = Ride.objects.all().delete()[0]
        
        # 3. Delete Users with safety filters
        # We exclude:
        # - Superusers (is_superuser=True)
        # - Users with role 'admin'
        # - Users with role 'administrator'
        users_to_delete = User.objects.exclude(
            Q(is_superuser=True) | 
            Q(role__iexact='admin') | 
            Q(role__iexact='administrator')
        )
        
        users_count = users_to_delete.delete()[0]
        
        self.stdout.write(self.style.SUCCESS(
            f"Cleanup Complete:\n"
            f"- {events_count} RideEvents deleted\n"
            f"- {rides_count} Rides deleted\n"
            f"- {users_count} Users deleted (Admins and Superusers preserved)"
        ))
