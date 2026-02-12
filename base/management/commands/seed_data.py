import random
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from base.models import Ride, RideEvent

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seeds high-volume data for performance testing'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        self.stdout.write(f"Starting performance seed at {now}")

        # 1. Create both Riders and Drivers
        riders = [User.objects.create_user(
            username=fake.unique.user_name(), email=fake.unique.email(),
            role='rider', phone_number=fake.numerify('##########')
        ) for _ in range(10)]
        
        drivers = [User.objects.create_user(
            username=fake.unique.user_name(), email=fake.unique.email(),
            role='driver', phone_number=fake.numerify('##########')
        ) for _ in range(5)]

        # 2. Create 20 Rides
        rides = []
        for _ in range(20):
            ride = Ride.objects.create(
                status=random.choice(['completed', 'en-route']),
                id_rider=random.choice(riders),
                id_driver=random.choice(drivers),
                pickup_latitude=float(fake.latitude()),
                pickup_longitude=float(fake.longitude()),
                dropoff_latitude=float(fake.latitude()),
                dropoff_longitude=float(fake.longitude()),
                pickup_time=now - timedelta(days=random.randint(1, 5))
            )
            rides.append(ride)

        # 3. Create 5,000 RideEvents with time distribution
        self.stdout.write("Generating 5,000 events...")
        events_to_create = []
        
        for i in range(5000):
            # Distribute events: 
            # 30% -> 24h ago | 30% -> 2 days ago | 40% -> 3-7 days ago
            rand = random.random()
            if rand < 0.3:
                offset = timedelta(hours=random.randint(0, 23)) # Within last 24h
            elif rand < 0.6:
                offset = timedelta(days=1, hours=random.randint(0, 23)) # 24-48h ago
            else:
                offset = timedelta(days=random.randint(2, 7)) # 2+ days ago

            event_time = now - offset
            
            events_to_create.append(RideEvent(
                id_ride=random.choice(rides),
                description=f"Performance Test Event {i}: {fake.sentence()}",
                created_at=event_time
            ))

            # Bulk create in batches of 1000 for efficiency
            if len(events_to_create) >= 1000:
                RideEvent.objects.bulk_create(events_to_create)
                events_to_create = []

        # Final batch
        if events_to_create:
            RideEvent.objects.bulk_create(events_to_create)

        self.stdout.write(self.style.SUCCESS("Successfully seeded 5,000 events!"))
