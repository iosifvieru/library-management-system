import libraryitems, datetime, user

class ItemFactory:
    def createItem(type: str, id:int, author:str, title: str, status: bool, publishDate: datetime, borrowedBy: int, noPages: int):
        if type == "book":
            return libraryitems.Book(id, author, title, status, publishDate, borrowedBy, noPages)


    def createUser(id: int, firstName: str,
                 lastName: str, city: str,
                 phoneNo: str, email: str, birthDate: datetime, borrowedBooks: list, adminLevel: int,
                 university: str, specialization: str, year: int):
        
        if not university or not specialization or not year:
            return user.BaseUser(id, firstName, lastName, city, phoneNo, email, birthDate, borrowedBooks, adminLevel)
        else :
            return user.Student(id, firstName, lastName, city, phoneNo, email, birthDate, borrowedBooks, adminLevel, university, specialization, year)
    # future developments