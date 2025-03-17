from django.contrib.auth import get_user_model
from django.db import models
from booking.validate import validate_start_date

User = get_user_model()

class Location(models.Model):
    title = models.CharField(max_length=100)  # Назва локації
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Ціна за бронювання
    is_available = models.BooleanField(default=True)  # Статус доступності локації
    capacity = models.IntegerField()  # Місткість локації
    description = models.TextField()  # Опис локації
    image_url = models.URLField(blank=True, null=True)  # URL зображення локації

    def __str__(self):
        return self.title  # Повертає назву локації

class Booking(models.Model):
    user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE)  # Користувач, який зробив бронювання
    location = models.ForeignKey(Location, related_name="locations", on_delete=models.CASCADE)  # Локація, для якої зроблено бронювання
    start_time = models.DateTimeField(validators=[validate_start_date])  # Дата початку бронювання з валідацією
    end_time = models.DateTimeField()  # Дата закінчення бронювання
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення бронювання
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Загальна ціна за бронювання
    confirmed = models.BooleanField(default=False)  # Статус підтвердження бронювання

    def __str__(self):
        return f"{self.user.username} - {self.location.title}"
