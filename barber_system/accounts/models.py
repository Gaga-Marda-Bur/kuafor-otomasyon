from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        name = self.user.get_full_name()
        if name.strip():
            return name
        return f"Müşteri #{self.id} ({self.user.username})"


class Employee(models.Model):
    ROLE_CHOICES = [
        ('barber', 'Berber'),
        ('hairdresser', 'Kuaför'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20)

    skills = models.CharField(max_length=255, blank=True)

    availability_start = models.TimeField(null=True, blank=True)
    availability_end = models.TimeField(null=True, blank=True)

    # ManyToManyField string ile tanımlanıyor
    services = models.ManyToManyField('salon.Service', blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    salon = models.ForeignKey('salon.Salon', on_delete=models.CASCADE, null=True, blank=True)  # Yeni alan

    def __str__(self):
        return f"Yönetici: {self.user.get_full_name()} - {self.salon.name if self.salon else 'Salon Atanmamış'}"
