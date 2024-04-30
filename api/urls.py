from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AcceptRideView,
    UserViewSet, RideStatusUpdateView,
    RideViewSet, 
)
from api.utils import availabe_drivers

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rides', RideViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rides/<int:ride_id>/update_status/', RideStatusUpdateView.as_view(), name='ride-update-status'),
    path('rides/<int:ride_id>/accept/', AcceptRideView.as_view(), name='accept_ride'),
    path('driver/<int:driver_id>/available/' ,availabe_drivers, name="availabe-drivers"),
    # path('cron-job',UpdateJob)
]