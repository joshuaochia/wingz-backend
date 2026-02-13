from django_filters import rest_framework as filters
from utils.annote import annotate_distance
from .models import Ride


class RideFilter(filters.FilterSet):
    # Standard filters
    status = filters.CharFilter(field_name="status", lookup_expr='exact')
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

        if lat and lng:
            qs = annotate_distance(qs, lat, lng)

        return qs
