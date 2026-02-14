# Django Ride Management API

A Django REST Framework application for managing ride events, rides, and users with advanced filtering, sorting, and geolocation features.

---

## Project Architecture

```
project/
├── app/
│   ├── settings/
│   │   ├── base.py          # Base settings shared across environments
│   │   ├── dev.py           # Development settings
│   │   └── prod.py          # Production settings
│   ├── asgi.py              # ASGI configuration
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── middleware.py        # Custom middleware (API logging)
│
├── base/
│   ├── management/
│   │   └── commands/
│   │       ├── clear_data.py    # Clear seeded data
│   │       └── seed_data.py     # Seed test data
│   ├── admin.py             # Django admin configuration
│   ├── tests/
│   │   └── test_ride_viewset.py
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models
│   ├── filters.py           # DRF filter classes
│   ├── paginations.py       # Custom pagination
│   ├── permissions.py       # Custom permissions
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URL patterns
│   └── views.py             # API views
│
├── schema/                  # DRF Spectacular schema configuration
├── scripts/
│   └── entrypoint.sh        # Docker entrypoint script
├── utils/                   # Helper functions and calculations
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── requirements.txt
└── README.md
```

---

## Prerequisites

- **Docker Engine**: v26.0.0 or higher
- **Docker Compose**: Latest version

No need to install Python, Django, or other dependencies locally - Docker handles everything!

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/joshuaochia/wingz-backend
cd wingz-backend
```

### 2. Build and Start Docker Containers

```bash
docker-compose -f docker-compose.yml up
```

> **Note**: Docker will automatically build the image if it's not found.

### 3. Access the Container Shell

Once the containers are running, open a new terminal and execute:

```bash
docker exec -it "container-id-here" sh
```

> **Tip**: Find your container ID with `docker ps`

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Seed Test Data

```bash
python manage.py seed_data
```

> **Important**: The seeded credentials will be displayed in the terminal. Save these for testing purposes and need to remove in production.

---

## API Documentation

### Base URL

```
http://localhost:8000
```

### Authentication

This project uses **dj-rest-auth** and **SimpleJWT** for authentication.

#### Login Endpoint

**POST** `/api/auth/login/`

**Request Body:**

```json
{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}
```

**Response:**

```json
{
  "access": "your_auth_token",
  "refresh": "your_refresh_token"
}
```

> **Note**: Use the credentials displayed after running `seed_data` command.

---

### Protected Endpoints

> **Authorization Required**: All API endpoints require admin authentication.
>
> Include the bearer in the request header:
>
> ```
> Authorization: Bearer <your_auth_token>
> ```

#### Get Users

**GET** `/api/base/users/`

Retrieves a list of all users.

---

#### Get Ride Events

**GET** `/api/base/ride-events/`

Retrieves a list of all ride events.

---

#### Get Rides

**GET** `/api/base/rides/`

Retrieves a list of all rides.

---

### Filtering

#### Filter by Status

**GET** `/api/base/rides/?status=en-route`

Available status values:

- `pending`
- `en-route`
- `completed`
- `cancelled`

#### Filter by Rider Email

**GET** `/api/base/rides/?rider_email=rider@example.com`

---

### Sorting

#### Sort by Distance (GPS Location)

**GET** `/api/base/rides/?status=en-route&lat=34.05&lng=-118.24&ordering=distance`

**Query Parameters:**

- `lat`: Latitude coordinate
- `lng`: Longitude coordinate
- `ordering`: Set to `distance` for proximity sorting

#### Sort by Pickup Time

**GET** `/api/base/rides/?ordering=pickup_time`

**Ordering Options:**

- `pickup_time`: Ascending order
- `-pickup_time`: Descending order

---

### View API Schema

**Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`

**ReDoc**: `http://localhost:8000/api/schema/redoc/`

---

**SQL Command for Reporting**

```sql
SELECT
    TO_CHAR(pickup_event.created_at, 'YYYY-MM') AS month,
    CONCAT(base_user.first_name, ' ', SUBSTRING(base_user.last_name, 1, 1)) AS driver,
    COUNT(*) AS trips_count_over_1hr
FROM
    ride
JOIN base_user
    ON ride.id_driver_id = base_user.id
JOIN base_rideevent pickup_event
    ON ride.id_ride = pickup_event.id_ride_id
   AND pickup_event.description = 'Status changed to pickup'
JOIN base_rideevent dropoff_event
    ON ride.id_ride = dropoff_event.id_ride_id
   AND dropoff_event.description = 'Status changed to dropoff'
   AND EXTRACT(EPOCH FROM (dropoff_event.created_at - pickup_event.created_at)) > 3600
GROUP BY
    TO_CHAR(pickup_event.created_at, 'YYYY-MM'),
    base_user.first_name,
    base_user.last_name
ORDER BY
    TO_CHAR(pickup_event.created_at, 'YYYY-MM') DESC,
    COUNT(*) DESC;
```
