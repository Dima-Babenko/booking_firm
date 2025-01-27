from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Location(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=False)
    capacity = models.IntegerField()
    description = models.TextField()

class Booking(models.Model):
    user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_name="locations", on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

