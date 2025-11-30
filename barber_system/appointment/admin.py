from django import forms
from django.contrib import admin
from .models import Appointment, Employee, Service


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1) Yeni randevu oluşturulurken
        if "service" in self.data:
            try:
                service_id = int(self.data.get("service"))
                self.fields["employee"].queryset = Employee.objects.filter(services=service_id)
            except:
                pass

        # 2) Randevu düzenlenirken
        elif self.instance.pk:
            service = self.instance.service
            self.fields["employee"].queryset = Employee.objects.filter(services=service)


class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentForm
    list_display = ("customer", "service", "employee", "date", "time", "status", "created_at")
    list_filter = ("status", "date", "employee", "service", "employee__salon")
    search_fields = ("customer__user__first_name", "customer__user__last_name", "employee__user__first_name")
    list_editable = ("status",)  #Doğrudan listeden düzenleme
    actions = ["approve_selected", "reject_selected"]  #Toplu aksiyonlar
    
    def approve_selected(self, request, queryset):
        """Seçili randevuları onayla"""
        updated = queryset.update(status='approved')
        self.message_user(request, f"{updated} randevu onaylandı.")
    approve_selected.short_description = "Seçili randevuları onayla"
    
    def reject_selected(self, request, queryset):
        """Seçili randevuları reddet"""
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} randevu reddedildi.")
    reject_selected.short_description = "Seçili randevuları reddet"
    
    # Tarih bazlı filtreleme
    date_hierarchy = 'date'


admin.site.register(Appointment, AppointmentAdmin)

