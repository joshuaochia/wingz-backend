from django_filters import rest_framework as filters
from utils.annote import annotate_distance
from .models import Ride


class RideFilter(filters.FilterSet):
    # Standard filters
    status = filters.CharFilter(field_name="status", lookup_expr='exact')
    rider_email = filters.CharFilter(field_name="id_rider__email", lookup_expr='icontains')

    class Meta:
        model = Ride
        fields = ['status', 'rider_email']

    @property
    def qs(self):
        """
        Override the queryset property to inject distance logic 
        before filtering/sorting happens.
        """
        parent_qs = super().qs
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        
        if lat and lng:
            return annotate_distance(parent_qs, lat, lng)
        return parent_qs
