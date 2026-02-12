from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Radians, Sin

def annotate_distance(queryset, lat, lng):
    """
    Annotates a queryset with a 'distance' field based on input GPS.
    """
    try:
        lat, lng = float(lat), float(lng)
        distance_expr = 6371 * ACos(
            Cos(Radians(lat)) * Cos(Radians(F('pickup_latitude'))) *
            Cos(Radians(F('pickup_longitude')) - Radians(lng)) +
            Sin(Radians(lat)) * Sin(Radians(F('pickup_latitude')))
        )
        return queryset.annotate(
            distance=ExpressionWrapper(distance_expr, output_field=FloatField())
        )
    except (ValueError, TypeError):
        return queryset
