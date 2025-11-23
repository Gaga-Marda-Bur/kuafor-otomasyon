class Appointment:
    _id_counter = 1

    def __init__(self, date, customer, employee, service):
        self.appointment_id = Appointment._id_counter
        Appointment._id_counter += 1
        self.date = date
        self.customer = customer
        self.employee = employee
        self.service = service

    def total_price(self):
        return self.service.calculate_price()

    def __str__(self):
        return (f"Appointment {self.appointment_id}: "
                f"{self.customer.name} with {self.employee.name} "
                f"for {self.service.name} on {self.date}")