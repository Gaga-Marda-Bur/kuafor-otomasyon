from person import Person

class Manager(Person):
    def __init__(self, name, phone):
        super().__init__(name, phone)
        self.role = "Manager"

    def __str__(self):
        return f"Salon Yöneticisi: {self.name}"