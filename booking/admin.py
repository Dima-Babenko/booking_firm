from django.contrib import admin
from booking.models import Location, Booking

# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'start_time', 'end_time', "created_at", 'total_price')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_available', 'capacity', 'description')

