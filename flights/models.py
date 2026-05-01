from django.db import models
import uuid
from django.contrib.auth.models import User

class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} - {self.code}"


class Flight(models.Model):
    origin = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="departures"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="arrivals"
    )
    duration = models.IntegerField()
    capacity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.origin} to {self.destination}"

class Passenger(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"{self.email} - {self.name}"

class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings", null=True, blank=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")
    booking_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
