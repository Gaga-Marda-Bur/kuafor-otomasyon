from django.contrib import admin
from .models import Salon, Service


class SalonAdmin(admin.ModelAdmin):
    list_display = ("name", "working_start", "working_end")
    search_fields = ("name",)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "salon", "duration", "price")
    search_fields = ("name", "salon__name")


admin.site.register(Salon, SalonAdmin)
admin.site.register(Service, ServiceAdmin)
