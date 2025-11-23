class Person:
    def __init__(self, name, phone):
        self._name = name
        self._phone = phone  # encapsulation

    @property
    def name(self):
        return self._name

    @property
    def phone(self):
        return self._phone

    def __str__(self):
        return f"{self._name} ({self._phone})"