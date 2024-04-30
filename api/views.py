import json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Ride
from .serializers import UserSerializer, RideSerializer,RideStatusUpdateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RideViewSet(viewsets.ModelViewSet):
    '''
        this class perform the services like 
        API endpoints for creating a ride request, viewing a ride's details, and listing all rides.
    '''
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    
    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = RideSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, reques):
        '''
            for listing all the rides
        '''
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        '''
            for retriving only one
        '''
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

class RideStatusUpdateView(APIView):
    '''
        this class is used for updating the status
    '''
    def patch(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RideStatusUpdateSerializer(ride, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AcceptRideView(APIView):
    def post(self, request, ride_id=None):
        ride_id = request.data.get('ride_id')
        driver_id = request.data.get('driver_id') # this we can take from session or from autheticated token and we will get the loggined driver user 
        try:
            ride = Ride.objects.get(id=ride_id, driver_id=None, status='REQUESTED')
        except Ride.DoesNotExist:
            return Response({'message': 'Ride request not found / already accepted'}, status=status.HTTP_400_BAD_REQUEST)

        ride.driver_id = driver_id
        ride.status = 'ACCEPTED'
        ride.save()

        serializer = RideSerializer(ride)
        return Response(serializer.data, status=status.HTTP_200_OK)