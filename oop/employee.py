from person import Person

class Employee(Person):
    _id_counter = 1

    def __init__(self, name, phone, role):
        super().__init__(name, phone)
        self.employee_id = Employee._id_counter
        Employee._id_counter += 1
        self.role = role

    def get_salary(self):
        """Polymorphism example"""
        if self.role == "Barber":
            return 15000
        elif self.role == "Kuaför":
            return 14000
        return 10000

    def __str__(self):
        return f"{self.role} {self.name} (ID: {self.employee_id})"