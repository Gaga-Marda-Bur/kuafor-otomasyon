class Salon:
    def __init__(self, salon_name):
        self.salon_name = salon_name
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
        return f"Salon: {self.salon_name}"