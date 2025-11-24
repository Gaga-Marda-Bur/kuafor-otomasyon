from person import Person

class Employee(Person):
    _id_counter = 1

    def __init__(self, name, phone, role):
        super().__init__(name, phone)
        self.employee_id = Employee._id_counter
        Employee._id_counter += 1
        
        self.role = role
        self.skills = []          # uzmanlık alanları
        self.services = []        # yapabildiği hizmetler
        self.availability = []    # ("10:00", "14:00") gibi

    def add_skill(self, skill):
        self.skills.append(skill)

    def add_service(self, service):
        self.services.append(service)

    def add_availability(self, start, end):
        self.availability.append((start, end))

    def is_available(self, time):
        """Çalışan o saatte uygun mu?"""
        for start, end in self.availability:
            if start <= time <= end:
                return True
        return False

    def __str__(self):
        return f"{self.role} {self.name} (ID: {self.employee_id})"
