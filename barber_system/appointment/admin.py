from django.contrib import admin
from .models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("customer", "employee", "service", "date", "time", "status")
    list_filter = ("status", "date", "employee")
    search_fields = ("customer__user__first_name", "customer__user__last_name", "employee__user__first_name")

admin.site.register(Appointment, AppointmentAdmin)
