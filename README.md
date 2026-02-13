Readme · MD
Copy

# Django Ride Management API

A Django REST Framework application for managing ride events, rides, and users with advanced filtering, sorting, and geolocation features.

## Table of Contents

- [Project Architecture](#project-architecture)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)

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
│   ├── apps.py              # App configuration
│   ├── models.py            # Database models
│   ├── filters.py           # DRF filter classes
│   ├── paginations.py       # Custom pagination
│   ├── permissions.py       # Custom permissions
│   ├── serializers.py       # DRF serializers
│   ├── tests.py             # Unit tests
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

This project uses **dj-rest-auth** for authentication.

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
  "key": "your_auth_token"
}
```

> **Note**: Use the credentials displayed after running `seed_data` command.

---

### Protected Endpoints

> **Authorization Required**: All API endpoints require admin authentication.
>
> Include the token in the request header:
>
> ```
> Authorization: Token <your_auth_token>
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

### Combined Filtering and Sorting

You can combine multiple query parameters:

**GET** `/api/base/rides/?status=en-route&rider_email=rider@example.com&ordering=pickup_time`

---

## Project Structure

### Settings Management

The project uses environment-specific settings:

- **base.py**: Common settings shared across all environments
- **dev.py**: Development-specific settings (Debug=True, local database)
- **prod.py**: Production-specific settings (Debug=False, security hardening)

### Custom Management Commands

- **seed_data**: Populates the database with test data for rapid development
- **clear_data**: Removes all seeded data from the database

### Middleware

- **API Logging Middleware**: Logs all API requests and responses for debugging and monitoring

---

## Development

### Creating Superuser

```bash
python manage.py createsuperuser
```

### Accessing Django Admin

Navigate to: `http://localhost:8000/admin/`

---

## API Schema

This project uses **DRF Spectacular** for API schema generation.

### View API Schema

**Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`

**ReDoc**: `http://localhost:8000/api/schema/redoc/`

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@db:5432/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Troubleshooting

### Container Won't Start

1. Check Docker logs:

   ```bash
   docker-compose logs
   ```

2. Rebuild containers:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

### Database Connection Issues

Ensure the database container is running:

```bash
docker ps
```

### Migration Errors

Reset migrations (development only):

```bash
python manage.py migrate --fake-initial
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

[Specify your license here]

---

## Support

For issues and questions, please open an issue in the repository.

---

## Acknowledgments

- Django REST Framework
- dj-rest-auth
- DRF Spectacular
- Docker

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
