from django.db import models
from accounts.models import Customer, Employee
from salon.models import Service
from datetime import timedelta, datetime
from django.core.exceptions import ValidationError


def add_minutes(base_time, minutes):
    """Saat + dakika eklemek için yardımcı fonksiyon"""
    full_datetime = datetime.combine(datetime.today(), base_time)
    new_datetime = full_datetime + timedelta(minutes=minutes)
    return new_datetime.time()


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    status_note = models.TextField(blank=True, null=True)

    def approve(self):
        """OOP'deki approve methodu"""
        self.status = 'approved'
        self.save()
    
    def reject(self):
        """OOP'deki reject methodu"""
        self.status = 'rejected'
        self.save()
    
    def check_collision(self):
        """OOP'deki check_collision methodu"""
        # Django'nun clean methodu zaten bunu yapıyor
        try:
            self.clean()
            return False  # No collision
        except ValidationError:
            return True  # Collision exists
    
    def check_employee_availability(self):
        """OOP'deki check_employee_availability methodu"""
        if self.employee.availability_start and self.employee.availability_end:
            return self.employee.availability_start <= self.time <= self.employee.availability_end
        return True
    
    def save(self, *args, **kwargs):
        """OOP'deki save methodu - validation ile"""
        # Django'nun clean methodunu çağır
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def appointment_id(self):
        """OOP'deki appointment_id property'si"""
        return self.id
    
    @property
    def datetime(self):
        """OOP'deki datetime property'si"""
        from django.utils import timezone
        return timezone.make_aware(
            timezone.datetime.combine(self.date, self.time)
        )

    def is_available(self):
        try:
            self.clean()
            return True
        except ValidationError:
            return False
    
    @property
    def end_time(self):
        # Service erişiminde hata almamak için güvenli erişim
        if self.service_id:
            return add_minutes(self.time, self.service.duration)
        return self.time

    def clean(self):
        """Hizmet süresine göre randevu çakışma ve uygunluk kontrolü"""

        # KRİTİK DÜZELTME:
        # Form validasyonundan geçemeyen alanlar (employee veya service) None olabilir.
        # Bu durumda 'self.employee' çağırmak 'RelatedObjectDoesNotExist' hatası verir.
        # Bu yüzden önce ID'lerin varlığını kontrol ediyoruz.
        if not self.employee_id or not self.service_id or not self.date or not self.time:
            return

        try:
            # duration'a erişmeyi dene
            duration = self.service.duration
        except Exception:
            return

        # Yeni randevunun başlangıç ve bitiş zamanları
        new_start = self.time
        new_end = add_minutes(self.time, duration)

        # Aynı çalışan ve aynı gün olan diğer randevular
        # Burada self.employee yerine self.employee_id kullanmak daha güvenlidir
        appointments = Appointment.objects.filter(
            employee_id=self.employee_id,
            date=self.date
        ).exclude(id=self.id)

        # Zaman çakışması kontrolü
        for appt in appointments:
            existing_start = appt.time
            existing_end = add_minutes(appt.time, appt.service.duration)

            # Çakışma varsa:
            if not (new_end <= existing_start or new_start >= existing_end):
                raise ValidationError("Bu çalışan bu zaman aralığında başka bir randevuya sahip.")

        # Çalışan uygunluk saat kontrolü
        try:
            employee = self.employee
            if employee.availability_start and employee.availability_end:
                if not (employee.availability_start <= self.time <= employee.availability_end):
                    raise ValidationError("Çalışan bu saatte uygun değil.")
        except Exception:
            pass

    def __str__(self):
        return f"{self.customer} - {self.service} @ {self.time}"