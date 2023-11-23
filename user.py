import datetime
from abc import ABC, abstractmethod


class User(ABC):
    @abstractmethod
    def borrowBook(self):
        pass

    @abstractmethod
    def returnBook(self):
        pass

    @abstractmethod
    def searchBook(self):
        pass

    @abstractmethod
    def displayCurrentBooks(self):
        pass


class BaseUser(User):
    def __init__(self, id: int, firstName: str,
                 lastName: str, city: str,
                 phoneNo: str, email: str, birthDate: datetime, borrowedBooks: list):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.city = city
        self.phoneNo = phoneNo
        self.email = email
        self.birthDate = birthDate
        self.borrowBooks = borrowedBooks

    def borrowBook(self):
        print("test")

    def returnBook(self):
        print("test")

    def searchBook(self):
        print("test")

    def displayCurrentBooks(self):
        print("test")

    def __str__(self):
        return f"id: {self.id}, firstName: {self.firstName}, lastName: {self.lastName}, " \
               f"city: {self.city}, phoneNo: {self.phoneNo}, email: {self.email}, " \
               f"birthDate: {self.birthDate}, borrowedBooks: {self.borrowBooks}"


class Student(BaseUser):
    def __init__(self, id: int, firstName: str,
                 lastName: str, city: str,
                 phoneNo: str, email: str, birthDate: datetime, borrowedBooks: list,
                 university: str, specialization: str, year: int):
        super().__init__(id, firstName, lastName, city, phoneNo, email, birthDate, borrowedBooks)
        self.univeristy = university
        self.specialization = specialization
        self.year = year

    def borrowBook(self):
        print("test")

    def returnBook(self):
        print("test")

    def searchBook(self):
        print("test")

    def displayCurrentBooks(self):
        print("test")

    def __str__(self):
        return f"{super().__str__()}, university: {self.univeristy}, specialization: {self.specialization}, year of Study: {self.year}"
    

class UserList:
    def __init__(self) -> None:
        self.items = list()

    def removeUser(self, id):
        self.items.pop(id)

    def updateList(self, user: User):
        self.items.append(user)
    
    def getUser(self, id: int):
        return self.items[id]