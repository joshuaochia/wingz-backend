from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Ride, RideEvent

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the Custom User model.
    """
    list_display = ('username', 'email', 'role', 'phone_number', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number')}),
    )

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Ride model.
    """
    list_display = ('id_ride', 'id_rider', 'id_driver', 'status', 'pickup_time', 'created_at')
    list_filter = ('status', 'pickup_time', 'created_at')
    search_fields = ('id_rider__username', 'id_driver__username', 'id_ride')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    """
    Admin configuration for the RideEvent model.
    """
    list_display = ('id_ride_event', 'id_ride', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('description', 'id_ride__id_ride')
    readonly_fields = ('created_at',)