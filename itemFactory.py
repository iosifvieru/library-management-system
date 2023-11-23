import libraryitems, datetime, user

class ItemFactory:
    def createItem(type: str, id:int, author:str, title: str, status: bool, publishDate: datetime, borrowedBy: int, noPages: int):
        if type == "book":
            return libraryitems.Book(id, author, title, status, publishDate, borrowedBy, noPages)

    # future developments