from django.shortcuts import render, redirect
from .models import Appointment
from salon.models import Service
from accounts.models import Employee
from django.http import JsonResponse
from datetime import datetime

def appointment_create(request):
    services = Service.objects.all()
    if request.method == 'POST':
        customer = request.user.customer
        service_id = request.POST.get('service')
        employee_id = request.POST.get('employee')
        date = request.POST.get('date')
        time = request.POST.get('time')

        service = Service.objects.get(id=service_id)
        employee = Employee.objects.get(id=employee_id)

        Appointment.objects.create(
            customer=customer,
            employee=employee,
            service=service,
            date=date,
            time=time
        )
        return redirect('home')

    return render(request, 'appointment_form.html', {'services': services})


def filter_employees(request):
    service_id = request.GET.get('service')
    service = Service.objects.get(id=service_id)
    employees = service.salon.employees.all()

    html = '<option value="">Seçiniz</option>'
    for emp in employees:
        html += f'<option value="{emp.id}">{emp.user.get_full_name()} ({emp.role})</option>'
    return JsonResponse({'html': html})


def available_times(request):
    employee_id = request.GET.get('employee')
    date_str = request.GET.get('date')

    employee = Employee.objects.get(id=employee_id)
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    # Çalışanın uygun saatleri
    start = employee.availability_start
    end = employee.availability_end

    # Mevcut randevular
    appointments = Appointment.objects.filter(employee=employee, date=date)
    booked_times = [appt.time.strftime("%H:%M") for appt in appointments]

    # Örnek: her 30 dakikada bir saat dilimi
    times = []
    t = datetime.combine(date, start)
    while t.time() <= end:
        time_str = t.time().strftime("%H:%M")
        if time_str not in booked_times:
            times.append(time_str)
        t = t.replace(minute=t.minute + 30)

    html = '<option value="">Seçiniz</option>'
    for t in times:
        html += f'<option value="{t}">{t}</option>'

    return JsonResponse({'html': html})
