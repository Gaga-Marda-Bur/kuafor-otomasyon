from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.user.get_full_name', read_only=True)
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'customer', 'employee', 'service', 'date', 'time', 'status',
            'customer_name', 'employee_name', 'service_name', 'created_at'
        ]