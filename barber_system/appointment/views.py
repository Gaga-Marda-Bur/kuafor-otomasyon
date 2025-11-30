from django.shortcuts import render, redirect
from .models import Appointment
from salon.models import Service
from accounts.models import Employee
from django.http import JsonResponse
from datetime import datetime
from .utils import get_available_times

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
    service_id = request.GET.get('service')  # Servis ID'sini de almalıyız

    # Eğer gerekli veriler yoksa boş dön
    if not (employee_id and date_str and service_id):
        return JsonResponse({'html': '<option value="">Lütfen seçimleri tamamlayın</option>'})

    try:
        employee = Employee.objects.get(id=employee_id)
        service = Service.objects.get(id=service_id)
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Senin yazdığın o harika utils fonksiyonunu burada kullanıyoruz
        # Bu fonksiyon dolu saatleri çıkarıp bize sadece uygun saatleri verecek.
        available_slots = get_available_times(employee, date_obj, service.duration)

        html = '<option value="">Saat Seçiniz</option>'
        for slot in available_slots:
            # slot bir time objesi olduğu için string'e çeviriyoruz
            time_str = slot.strftime("%H:%M")
            html += f'<option value="{time_str}">{time_str}</option>'
            
    except Exception as e:
        print(f"Hata: {e}")
        html = '<option value="">Hata oluştu</option>'

    return JsonResponse({'html': html})