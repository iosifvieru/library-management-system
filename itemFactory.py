import libraryitems, datetime, user

class ItemFactory:
    def createItem(type: str, id:int, author:str, title: str, status: bool, publishDate: datetime, borrowedBy: int, noPages: int):
        if type == "book":
            return libraryitems.Book(id, author, title, status, publishDate, borrowedBy, noPages)

    
    def createUser(type: str, id: int, firstName:str, lastName: str, city: str, 
                   phoneNo: str, email:str, birthDate: datetime, borrowedBooks: list):
        
        if type == "user":
            return user.BaseUser(id, firstName, lastName, city, phoneNo, email, birthDate, borrowedBooks)
        
    # future developments