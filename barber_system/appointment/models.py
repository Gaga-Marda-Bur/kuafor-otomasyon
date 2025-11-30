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
    created_at = models.DateTimeField(auto_now_add=True)  # Yeni
    updated_at = models.DateTimeField(auto_now=True)      # Yeni
    
    # Onay/Red sebebi
    status_note = models.TextField(blank=True, null=True)  # Yeni

    def approve(self, note=""):
        """Randevuyu onayla"""
        self.status = 'approved'
        self.status_note = note
        self.save()
    
    def reject(self, note=""):
        """Randevuyu reddet"""
        self.status = 'rejected'
        self.status_note = note
        self.save()

    def is_available(self):
        """Randevu zamanı müsait mi kontrol et"""
        # Mevcut clean mantığı buraya taşınabilir
        try:
            self.clean()
            return True
        except ValidationError:
            return False
    
    @property
    def end_time(self):
        """Randevu bitiş zamanını hesapla"""
        return add_minutes(self.time, self.service.duration)
    

    def clean(self):
        """Hizmet süresine göre randevu çakışma ve uygunluk kontrolü"""

        # Yeni randevunun başlangıç ve bitiş zamanları
        new_start = self.time
        new_end = add_minutes(self.time, self.service.duration)

        # Aynı çalışan ve aynı gün olan diğer randevular
        appointments = Appointment.objects.filter(
            employee=self.employee,
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
        if self.employee.availability_start and self.employee.availability_end:
            if not (self.employee.availability_start <= self.time <= self.employee.availability_end):
                raise ValidationError("Çalışan bu saatte uygun değil.")

    def __str__(self):
        return f"{self.customer} - {self.service} @ {self.time}"
