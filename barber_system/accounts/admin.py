from django.contrib import admin
from .models import Customer, Employee, Manager


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("get_name", "role", "phone", "availability_start", "availability_end", "skills")
    search_fields = ("user__first_name", "user__last_name", "role")
    list_filter = ("role",)

    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = "Çalışan Adı"


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("get_name", "phone")
    search_fields = ("user__first_name", "user__last_name")

    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = "Müşteri"

class ManagerAdmin(admin.ModelAdmin):
    list_display = ("get_name", "phone", "salon")
    search_fields = ("user__first_name", "user__last_name", "salon__name")
    
    def get_name(self, obj):
        return obj.user.get_full_name()
    get_name.short_description = "Yönetici Adı"

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Manager, ManagerAdmin)
