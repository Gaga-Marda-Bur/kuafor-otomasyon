from django.db import models
from accounts.models import Employee

class Salon(models.Model):
    name = models.CharField(max_length=100)
    working_start = models.TimeField()
    working_end = models.TimeField()

    employees = models.ManyToManyField(Employee, blank=True)

    def __str__(self):
        return self.name



class Service(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration = models.IntegerField()  # dakika
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.price} TL)"
