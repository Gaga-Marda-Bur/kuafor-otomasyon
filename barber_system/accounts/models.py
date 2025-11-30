from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def get_appointment_history(self):
        """Müşterinin randevu geçmişi"""
        return self.appointment_set.all().order_by('-date', '-time')
    
    def get_pending_appointments(self):
        """Bekleyen randevular - OOP'deki status kontrolü"""
        return self.appointment_set.filter(status='pending')
    
    def get_approved_appointments(self):
        """Onaylanmış randevular"""
        return self.appointment_set.filter(status='approved')
    
    @property
    def customer_id(self):
        """OOP'deki customer_id property'si"""
        return self.id

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

    def add_skill(self, skill):
        """OOP'deki add_skill methodu"""
        skills_list = self.get_skills_list()
        if skill not in skills_list:
            skills_list.append(skill)
            self.skills = ', '.join(skills_list)
            self.save()
    
    def add_service(self, service):
        """OOP'deki add_service methodu"""
        self.services.add(service)
    
    def add_availability(self, start_time, end_time):
        """OOP'deki add_availability methodu"""
        self.availability_start = start_time
        self.availability_end = end_time
        self.save()
    
    def is_available(self, time_str):
        """OOP'deki is_available methodu"""
        from django.utils.dateparse import parse_time
        
        time_obj = parse_time(time_str)
        if not time_obj:
            return False
            
        if self.availability_start and self.availability_end:
            return self.availability_start <= time_obj <= self.availability_end
        return True
    
    def get_skills_list(self):
        """Skills string'ini liste olarak döndür"""
        return [skill.strip() for skill in self.skills.split(',')] if self.skills else []
    
    @property
    def employee_id(self):
        """OOP'deki employee_id property'si"""
        return self.id

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    salon = models.ForeignKey('salon.Salon', on_delete=models.CASCADE, null=True, blank=True)  # Yeni alan

    def __str__(self):
        return f"Yönetici: {self.user.get_full_name()} - {self.salon.name if self.salon else 'Salon Atanmamış'}"
