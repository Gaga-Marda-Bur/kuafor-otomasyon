from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Salon

def home(request):
    salons = Salon.objects.all()
    today = timezone.now().date()  # Bugünün tarihini ekleyin
    
    # Kullanıcı istatistikleri için güvenli yaklaşım
    context = {
        'salons': salons,
        'today': today,
    }
    
    # Eğer kullanıcı giriş yapmışsa ve customer profili varsa
    if request.user.is_authenticated and hasattr(request.user, 'customer'):
        customer = request.user.customer
        appointments = customer.appointment_set.all()
        
        context.update({
            'total_appointments': appointments.count(),
            'pending_appointments': appointments.filter(status='pending').count(),
            'approved_appointments': appointments.filter(status='approved').count(),
        })
    else:
        context.update({
            'total_appointments': 0,
            'pending_appointments': 0,
            'approved_appointments': 0,
        })
    
    return render(request, 'home.html', context)

def salon_detail(request, pk):
    salon = get_object_or_404(Salon, pk=pk)
    return render(request, 'salon_detail.html', {'salon': salon})