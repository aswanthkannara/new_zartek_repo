from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from .choices import STATUS_CHOICES
from django.contrib.auth.models import AbstractUser

class DriverUser(models.Model):
    driver_name = models.CharField(max_length=255)
    mobie_number = models.CharField(max_length=255)
    is_active = models.BooleanField(null=True,blank=True)
    is_staff = models.BooleanField(null=True,blank=True)
    sex = models.IntegerField(null=True, blank=True)
    current_location = models.CharField(max_length=255)


class Ride(models.Model):
    rider = models.ForeignKey(User, related_name='rides_as_rider', on_delete=models.CASCADE)
    driver = models.ForeignKey(DriverUser, related_name='rides_as_driver', on_delete=models.CASCADE, null=True, blank=True)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    current_location = models.CharField(max_length=255, blank=True, null=True)

    def update_location(self, new_location):
        pass
        # self.current_location = new_location
        # self.save()
        # offset = 0.001  # Adjust the offset to control the distance moved
        # lat, lon = self.current_location.split(',')
        # new_lat = float(lat) + random.uniform(-offset, offset)
        # new_lon = float(lon) + random.uniform(-offset, offset)
        # self.current_location = f"{new_lat},{new_lon}"
        # self.save()