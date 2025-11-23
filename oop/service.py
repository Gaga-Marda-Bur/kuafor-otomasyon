class Service:
    def __init__(self, name, duration, base_price):
        self.name = name
        self.duration = duration
        self.base_price = base_price

    def calculate_price(self):
        """Polymorphism example"""
        return self.base_price

    def __str__(self):
        return f"{self.name} - {self.duration} min - {self.base_price} TL"