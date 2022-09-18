from database.model import Model
from flask_login import UserMixin


class Customer(UserMixin, Model):
    def __init__(self, id, firstName, patronymic, lastName, birthDate, email, phoneNumber, password):
        super().__init__()
        self.id = id
        self.firstName = firstName
        self.patronymic = patronymic
        self.lastName = lastName
        self.birthDate = birthDate
        self.email = email
        self.phoneNumber = phoneNumber
        self.password = password