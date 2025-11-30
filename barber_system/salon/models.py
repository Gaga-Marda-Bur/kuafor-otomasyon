from django.db import models
from accounts.models import Employee
from barber_system.appointment.models import Appointment

class Salon(models.Model):
    name = models.CharField(max_length=100)
    working_start = models.TimeField()
    working_end = models.TimeField()
    address = models.TextField(blank=True)  
    phone = models.CharField(max_length=20, blank=True)  
    description = models.TextField(blank=True)  

    employees = models.ManyToManyField(Employee, blank=True)

    def get_available_employees(self, service, date, time):
        """Belirli bir hizmet, tarih ve saat için uygun çalışanları getir"""
        from appointment.models import add_minutes
        
        end_time = add_minutes(time, service.duration)
        
        # Bu hizmeti verebilen çalışanlar
        qualified_employees = self.employees.filter(services=service)
        
        available_employees = []
        for employee in qualified_employees:
            # Uygunluk saat kontrolü
            if (employee.availability_start and employee.availability_end):
                if not (employee.availability_start <= time <= employee.availability_end):
                    continue
            
            # Randevu çakışma kontrolü
            conflicting_appointments = Appointment.objects.filter(
                employee=employee,
                date=date,
                status__in=['pending', 'approved']
            )
            
            has_conflict = False
            for appt in conflicting_appointments:
                appt_end = add_minutes(appt.time, appt.service.duration)
                if not (end_time <= appt.time or time >= appt_end):
                    has_conflict = True
                    break
            
            if not has_conflict:
                available_employees.append(employee)
        
        return available_employees

    def __str__(self):
        return self.name



class Service(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration = models.IntegerField()  # dakika
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.price} TL)"
