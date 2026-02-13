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
