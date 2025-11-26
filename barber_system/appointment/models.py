from django.db import models
from accounts.models import Customer, Employee
from salon.models import Service

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def clean(self):
        """Çakışma kontrolü"""
        same_time = Appointment.objects.filter(
            employee=self.employee,
            date=self.date,
            time=self.time,
        ).exists()

        if same_time:
            raise ValueError("Bu çalışan bu saatte zaten randevuya sahip.")

        """Uygunluk kontrolü"""
        if self.employee.availability_start and self.employee.availability_end:
            if not (self.employee.availability_start <= self.time <= self.employee.availability_end):
                raise ValueError("Çalışan bu saatte uygun değil.")

    def __str__(self):
        return f"{self.customer} - {self.service} @ {self.time}"
