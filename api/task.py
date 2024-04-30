from background_task import background
from django_cron import CronJobBase, Schedule
from .models import Ride

# @background(schedule=10)
# def update_ride_location():
#     ride = Ride.objects.get(id=1)
#     new_location = '1233'
#     ride.update_location(new_location)

class UpdateJob(CronJobBase):
    '''
        for updating the location with every one minute.
        !! google map api is not getting for my account thats why i used this!! 
    '''
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    def do(self):
        ride = Ride.objects.get(id=1)
        new_location = 'mavoor'
        ride.update_location(new_location)

    