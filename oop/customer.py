from person import Person

class Customer(Person):
    _id_counter = 1

    def __init__(self, name, phone):
        super().__init__(name, phone)
        self.customer_id = Customer._id_counter
        Customer._id_counter += 1
        self.history = []  # previous appointments

    def add_history(self, appointment):
        self.history.append(appointment)

    def __str__(self):
        return f"Customer {self.customer_id}: {self.name}"
