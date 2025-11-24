class Appointment:
    _id_counter = 1
    all_appointments = []   # sistemdeki tüm randevular

    def __init__(self, datetime, customer, employee, service):
        self.appointment_id = Appointment._id_counter
        Appointment._id_counter += 1
        
        self.datetime = datetime
        self.customer = customer
        self.employee = employee
        self.service = service
        
        self.status = "pending"   # pending, approved, rejected

    def approve(self):
        self.status = "approved"

    def reject(self):
        self.status = "rejected"

    def check_collision(self):
        """Aynı çalışanın aynı zamanda başka randevusu var mı?"""
        for a in Appointment.all_appointments:
            if a.employee == self.employee and a.datetime == self.datetime:
                return True
        return False

    def check_employee_availability(self):
        """Çalışanın uygun olduğu zaman aralığında mı?"""
        time = self.datetime.split(" ")[1]  # "2025-05-17 10:30"
        return self.employee.is_available(time)

    def save(self):
        """Randevu validasyon"""
        if self.check_collision():
            return "Çakışma: Bu çalışan aynı saatte başka randevuya sahip!"
        
        if not self.check_employee_availability():
            return "Çalışan bu saatte uygun değil!"
        
        self.approve()
        Appointment.all_appointments.append(self)
        return "Randevu başarıyla oluşturuldu ve onaylandı."

    def __str__(self):
        return (f"Appointment {self.appointment_id}: "
                f"{self.customer.name} - {self.service.name} ({self.datetime}) "
                f"[{self.status}]")
