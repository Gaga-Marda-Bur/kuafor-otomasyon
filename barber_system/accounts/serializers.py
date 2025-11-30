from rest_framework import serializers
from .models import Employee, Customer

class EmployeeSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'user_full_name', 'user_username', 'role', 'phone', 'skills', 'availability_start', 'availability_end']

class CustomerSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'user_full_name', 'user_username', 'phone']