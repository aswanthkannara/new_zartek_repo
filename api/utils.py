from api.models import Ride
from .models import DriverUser
from django.http import JsonResponse
from rest_framework import status
from geopy.distance import geodesic
from django.views.decorators.csrf import csrf_exempt

def match_driver_to_ride(ride_request):
    available_drivers = DriverUser.objects.filter(
        is_active=True,
        is_staff = True,
        current_location=(ride_request.pickup_location)
    )

    for driver in available_drivers:
        driver.distance_to_pickup = geodesic(
            (driver.current_location.latitude, driver.current_location.longitude),
            (ride_request.pickup_location.latitude, ride_request.pickup_location.longitude)
        ).kilometers

    sorted_drivers = sorted(available_drivers, key=lambda d: d.distance_to_pickup)

    if sorted_drivers:
        nearest_driver = sorted_drivers[0]
        return nearest_driver
    else:
        return None

@csrf_exempt
def availabe_drivers(request,driver_id=None):
    ride_request = Ride.objects.get(pk=driver_id)
    matched_driver = match_driver_to_ride(ride_request)
    if matched_driver:
        ride_request.driver = matched_driver
        ride_request.status = 'accepted'
        ride_request.save()
        return JsonResponse({'available drivers': matched_driver}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'No active drivers in this circle'}, status=status.HTTP_404_NOT_FOUND)
