from rest_framework import serializers
from .models import Flight, Ticket

from django.contrib.auth.models import User

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def validate(self, data):
        # Check if the seat is already booked
        if Ticket.objects.filter(flight=data['flight'], seat_number=data['seat_number']).exists():
            raise serializers.ValidationError('This seat is already booked.')
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ['email','username','password','id']