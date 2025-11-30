from django.shortcuts import render, redirect
from django.http import HttpResponse  # JsonResponse yerine bunu kullanıyoruz
from .models import Appointment
from salon.models import Service
from accounts.models import Employee
from datetime import datetime
from .utils import get_available_times

def appointment_create(request):
    services = Service.objects.all()
    employees = Employee.objects.all()  # Tous les employés pour l'initialisation
    
    if request.method == 'POST':
        if hasattr(request.user, 'customer'):
            customer = request.user.customer
        else:
            return redirect('home')

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

    # CORRECTION: 'employees' au lieu de 'employee'
    return render(request, 'appointment_form.html', {
        'services': services, 
        'employees': employees  # Variable corrigée
    })


def filter_employees(request):
    service_id = request.GET.get('service')
    
    if not service_id:
        return HttpResponse('<option value="">Önce hizmet seçiniz</option>')

    try:
        # Filtrer les employés qui peuvent fournir ce service
        employees = Employee.objects.filter(services__id=service_id).distinct()
        
        if not employees.exists():
            return HttpResponse('<option value="">Bu hizmeti verebilecek çalışan bulunmamaktadır</option>')

        html = '<option value="">Çalışan Seçiniz</option>'
        for emp in employees:
            full_name = emp.user.get_full_name()
            display_name = f"{full_name} ({emp.role})" if full_name else f"{emp.user.username} ({emp.role})"
            html += f'<option value="{emp.id}">{display_name}</option>'
        
        return HttpResponse(html)
        
    except Exception as e:
        print(f"Hata: {e}")
        return HttpResponse('<option value="">Hata oluştu</option>')


def available_times(request):
    employee_id = request.GET.get('employee')
    date_str = request.GET.get('date')
    service_id = request.GET.get('service')

    if not (employee_id and date_str and service_id):
        return HttpResponse('<option value="">Seçimler eksik</option>')

    try:
        employee = Employee.objects.get(id=employee_id)
        service = Service.objects.get(id=service_id)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Utils fonksiyonu ile uygun saatleri hesapla
        available_slots = get_available_times(employee, date_obj, service.duration)

        html = '<option value="">Saat Seçiniz</option>'
        for slot in available_slots:
            time_str = slot.strftime("%H:%M")
            html += f'<option value="{time_str}">{time_str}</option>'
            
    except Exception as e:
        print(f"Hata: {e}")
        html = '<option value="">Hata oluştu</option>'

    # Burada da HTML döndürüyoruz
    return HttpResponse(html)