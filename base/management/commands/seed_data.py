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

        # 0. Create one Admin Superuser
        admin_email = "admin@example.com"
        admin_username = "admin"
        admin_password = "admin123"

        admin_user, created = User.objects.get_or_create(
            email=admin_email,
            defaults={
                "username": admin_username,
                "first_name": "Admin",
                "last_name": "User",
                "role": "admin",
                "is_staff": True,
                "is_superuser": True,
            }
        )

        self.stdout.write(self.style.NOTICE(
            "\nADMIN LOGIN DETAILS\n"
            "-------------------\n"
            f"Username : {admin_username}\n"
            f"Email    : {admin_email}\n"
            f"Password : {admin_password}\n"
            "Role     : admin\n"
        ))

        if created:
            admin_user.set_password(admin_password)
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Admin superuser created"))
        else:
            self.stdout.write(self.style.WARNING("Admin superuser already exists"))


        # 1. Create both Riders and Drivers
        riders = [User.objects.create_user(
            username=fake.unique.user_name(), email=fake.unique.email(),
            role='rider', phone_number=fake.numerify('##########'),
            first_name=fake.first_name(), last_name=fake.last_name()
        ) for _ in range(10)]
        
        drivers = [User.objects.create_user(
            username=fake.unique.user_name(), email=fake.unique.email(),
            role='driver', phone_number=fake.numerify('##########'),
            first_name=fake.first_name(), last_name=fake.last_name()
        ) for _ in range(5)]

        # 2. Create 20 Rides with pickup/dropoff events
        rides = []
        
        # Only 3-5 rides will qualify (>1 hour)
        qualifying_ride_indices = random.sample(range(20), k=random.randint(3, 5))
        
        for i in range(20):
            # Determine pickup time - spread across last 60 days with varied times
            total_minutes_ago = random.randint(60, 86400)  # 1 hour to 60 days in minutes
            pickup_time = now - timedelta(minutes=total_minutes_ago)
            
            ride = Ride.objects.create(
                status=random.choice(['completed', 'en-route']),
                id_rider=random.choice(riders),
                id_driver=random.choice(drivers),
                pickup_latitude=float(fake.latitude()),
                pickup_longitude=float(fake.longitude()),
                dropoff_latitude=float(fake.latitude()),
                dropoff_longitude=float(fake.longitude()),
                pickup_time=pickup_time
            )
            rides.append(ride)
            
            # Create pickup event
            pickup_event = RideEvent.objects.create(
                id_ride=ride,
                description='Status changed to pickup'
            )
            # Update the timestamp
            RideEvent.objects.filter(id_ride_event=pickup_event.id_ride_event).update(
                created_at=pickup_time
            )
            
            # Create dropoff event
            # Only qualifying rides get >1 hour duration
            if i in qualifying_ride_indices:
                # Trip duration between 1.5 to 4 hours (QUALIFIES)
                trip_duration_minutes = random.randint(90, 240)  # 1.5-4 hours
            else:
                # Trip duration less than 1 hour (does NOT qualify)
                trip_duration_minutes = random.randint(5, 58)  # 5-58 minutes
            
            dropoff_time = pickup_time + timedelta(minutes=trip_duration_minutes)
            
            dropoff_event = RideEvent.objects.create(
                id_ride=ride,
                description='Status changed to dropoff'
            )
            # Update the timestamp
            RideEvent.objects.filter(id_ride_event=dropoff_event.id_ride_event).update(
                created_at=dropoff_time
            )

        # 3. Create additional random events (60 more to reach ~100 total)
        self.stdout.write("Generating additional events...")
        
        for i in range(60):
            # Random time in the past (up to 60 days)
            minutes_ago = random.randint(60, 86400)  # 1 hour to 60 days
            event_time = now - timedelta(minutes=minutes_ago)
            
            event = RideEvent.objects.create(
                id_ride=random.choice(rides),
                description=f"Additional Event {i}: {fake.sentence()}"
            )
            # Update the timestamp
            RideEvent.objects.filter(id_ride_event=event.id_ride_event).update(
                created_at=event_time
            )

        total_events = 20 * 2 + 60  # pickup + dropoff for each ride + additional events
        
        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded data!\n"
            f"- {len(riders)} riders\n"
            f"- {len(drivers)} drivers\n"
            f"- {len(rides)} rides\n"
            f"- {total_events} events\n"
            f"- {len(qualifying_ride_indices)} rides with trips > 1 hour (qualifying results)"
        ))