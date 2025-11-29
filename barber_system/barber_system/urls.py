from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('salon.urls')),         # Salon ve home sayfası
    path('appointments/', include('appointment.urls')),  # Randevular
    path('accounts/', include('accounts.urls')),        # Login, logout, register
]
