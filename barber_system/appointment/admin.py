from django import forms
from django.contrib import admin
from .models import Appointment, Employee, Service

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1) Eğer formda veri varsa (POST işlemi yapıldıysa)
        if self.data.get("service"):
            try:
                service_id = int(self.data.get("service"))
                # Seçilen hizmete göre çalışanları filtrele
                self.fields["employee"].queryset = Employee.objects.filter(services=service_id)
            except (ValueError, TypeError):
                pass
        
        # 2) Mevcut bir randevu düzenleniyorsa
        elif self.instance.pk and self.instance.service:
            self.fields["employee"].queryset = Employee.objects.filter(services=self.instance.service)
        
        # 3) Hiçbir şey seçili değilse çalışan listesini boş getir (veya hepsini getir)
        else:
            # İstersen burayı boş bırakabilirsin: Employee.objects.none()
            pass

class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentForm
    # Hizmeti çalışandan önce göstermek, mantıksal akış için daha doğru
    fields = ('customer', 'service', 'employee', 'date', 'time', 'status', 'status_note')
    
    list_display = ("customer", "service", "employee", "date", "time", "status", "created_at")
    list_filter = ("status", "date", "employee", "service")
    search_fields = ("customer__user__first_name", "customer__user__last_name")
    list_editable = ("status",)
    
admin.site.register(Appointment, AppointmentAdmin)