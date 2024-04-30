from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ride

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'

    def create(self, validated_data):
        rider_id = validated_data.pop('rider')
        print('rider_id',rider_id)
        # rider = User.objects.get(id=rider_id)
        ride = Ride.objects.create(rider=rider_id, **validated_data)
        return ride
    
class RideStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['status']