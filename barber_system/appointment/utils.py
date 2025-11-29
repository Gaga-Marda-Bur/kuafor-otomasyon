from datetime import datetime, timedelta

def get_available_times(employee, date, service_duration):
    """
    employee: Employee objesi
    date: datetime.date objesi
    service_duration: dakika
    return: boş zaman listesi [(14:00, 14:30), ...]
    """

    start = datetime.combine(date, employee.availability_start)
    end = datetime.combine(date, employee.availability_end)
    step = timedelta(minutes=15)  # zaman adımı (isteğe göre 5-10-15 dk)

    # Çalışanın randevuları
    appointments = employee.appointment_set.filter(date=date)

    busy_times = []
    for appt in appointments:
        appt_start = datetime.combine(date, appt.time)
        appt_end = appt_start + timedelta(minutes=appt.service.duration)
        busy_times.append((appt_start, appt_end))

    available_times = []
    current = start
    while current + timedelta(minutes=service_duration) <= end:
        current_end = current + timedelta(minutes=service_duration)
        overlap = False
        for busy_start, busy_end in busy_times:
            if not (current_end <= busy_start or current >= busy_end):
                overlap = True
                break
        if not overlap:
            available_times.append(current.time())
        current += step

    return available_times
