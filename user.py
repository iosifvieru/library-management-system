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
    def displayCurrentBooks(self):
        pass


class BaseUser(User):
    def __init__(self, id: int, firstName: str,
                 lastName: str, city: str,
                 phoneNo: str, email: str, birthDate: datetime, borrowedBooks: list, adminLevel: int):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.city = city
        self.phoneNo = phoneNo
        self.email = email
        self.birthDate = birthDate
        self.borrowBooks = borrowedBooks
        self.adminLevel = adminLevel

    def borrowBook(self, book):
        self.borrowBooks.append(book)

    def returnBook(self, book):
        id = self.borrowBooks.index(book)
        self.borrowBooks.pop(id)

    def displayCurrentBooks(self):
        return self.borrowBooks

    def getID(self):
        return self.id

    def __str__(self):
        return f"id: {self.id}, firstName: {self.firstName}, lastName: {self.lastName}, " \
               f"city: {self.city}, phoneNo: {self.phoneNo}, email: {self.email}, " \
               f"birthDate: {self.birthDate}, borrowedBooks: {self.borrowBooks}"

    def getAdminLevel(self):
        return self.adminLevel

class Student(BaseUser):
    def __init__(self, id: int, firstName: str,
                 lastName: str, city: str,
                 phoneNo: str, email: str, birthDate: datetime, borrowedBooks: list, adminLevel: int,
                 university: str, specialization: str, year: int):
        super().__init__(id, firstName, lastName, city, phoneNo, email, birthDate, borrowedBooks, adminLevel)
        self.univeristy = university
        self.specialization = specialization
        self.year = year

    def borrowBook(self):
        super().borrowBook()

    def returnBook(self):
        super().returnBook()

    def displayCurrentBooks(self):
        super().displayCurrentBooks()

    def __str__(self):
        return f"{super().__str__()}, university: {self.univeristy}, specialization: {self.specialization}, year of Study: {self.year}"
    
    def getAdminLevel(self):
        super().getAdminLevel()

class UserList:
    def __init__(self) -> None:
        self.items = list()

    def removeUser(self, id):
        tempUser = self.getUser(id)
        user_id = self.items.index(tempUser)
        # print(user_id)
        self.items.pop(user_id)
        

    def addUser(self, user: User):
        self.items.append(user)
    
    def getUser(self, id: int):
        for user in self.items:
            if user.getID() == id:
                return user
        
        return None
    
    def __str__(self):
        user_strings = [str(user) for user in self.items]
        return "\n".join(user_strings)
