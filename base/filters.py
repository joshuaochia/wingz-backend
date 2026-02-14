from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
from utils.annote import annotate_distance
from .models import Ride


class RideFilter(filters.FilterSet):
    # Standard filters
    status = filters.ChoiceFilter(
        field_name="status",
        lookup_expr='exact',
        choices=Ride.STATUS_CHOICES,
        help_text="Filter by ride status"
    )
    rider_email = filters.CharFilter(field_name="id_rider__email", lookup_expr='icontains')

    class Meta:
        model = Ride
        fields = []

    def filter_queryset(self, queryset):
        """
        Override the queryset property to inject distance logic 
        before filtering/sorting happens.
        """
        qs = super().filter_queryset(queryset)

        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')

        # Both or neither - prevent partial coordinates
        if bool(lat) != bool(lng):
            raise ValidationError({'coordinates': 'Both lat and lng are required together'})

        if lat and lng:
            # Validate ranges
            try:
                lat_f, lng_f = float(lat), float(lng)
                if not (-90 <= lat_f <= 90 and -180 <= lng_f <= 180):
                    raise ValueError
            except (ValueError, TypeError):
                raise ValidationError({'coordinates': 'Invalid coordinates. Lat: -90 to 90, Lng: -180 to 180'})
            
            qs = annotate_distance(qs, lat_f, lng_f)

        return qs
