from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from salon.api import SalonViewSet, ServiceViewSet
from accounts.api import EmployeeViewSet, CustomerViewSet
from appointment.api import AppointmentViewSet

router = DefaultRouter()
router.register(r'salons', SalonViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'appointments', AppointmentViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('salon.urls')),         # Salon ve home sayfası
    path('appointments/', include('appointment.urls')),  # Randevular
    path('accounts/', include('accounts.urls')),        # Login, logout, register
    
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
