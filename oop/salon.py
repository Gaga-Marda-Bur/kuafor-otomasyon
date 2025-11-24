class Salon:
    def __init__(self, salon_name, working_hours=None):
        self.salon_name = salon_name
        
        # working_hours = ("09:00", "20:00")
        self.working_hours = working_hours or ("09:00", "20:00")
        
        self.employees = []
        self.customers = []
        self.services = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def add_customer(self, customer):
        self.customers.append(customer)

    def add_service(self, service):
        self.services.append(service)

    def __str__(self):
        return f"Salon: {self.salon_name} (Çalışma: {self.working_hours[0]} - {self.working_hours[1]})"
