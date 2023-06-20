from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    pass 

class Airport(models.Model):
    city = models.CharField(max_length=100)
    code = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField(default=130)

    def __str__(self):
        return f"{self.origin.city} --> {self.destination.city}"

class Passenger(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    flight = models.ManyToManyField(Flight, related_name="passengers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"