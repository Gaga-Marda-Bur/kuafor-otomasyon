from rest_framework import serializers
from .models import Salon, Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'salon', 'name', 'duration', 'price']

class SalonSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Salon
        fields = ['id', 'name', 'working_start', 'working_end', 'address', 'phone', 'description', 'services']