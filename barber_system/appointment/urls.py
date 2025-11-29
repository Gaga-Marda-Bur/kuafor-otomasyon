from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.appointment_create, name='appointment_create'),
    path('filter-employees/', views.filter_employees, name='filter_employees'),
    path('available-times/', views.available_times, name='available_times'),
]
