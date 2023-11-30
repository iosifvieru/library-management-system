import libraryitems
import database, datetime, itemFactory

class Library:
    def __init__(self):
        self.items = list()

    def print(self):
        result_string = '\n'.join(book.__str__() for book in self.items)
        return result_string

    def getBooks(self):
        tempList = list()
        for book in self.items:
            tempList.append(book)
        
        return tempList
        

class LibraryController:
    __last_id = 1

    @staticmethod
    def addBook(library: Library, book: libraryitems.Book):
        library.items.append(book)

    # functie de updateBooks
    # am ales sa folosesc o variabila statica __last_id pt. a eficientiza actualizarea in cazul in care se va adauga o carte noua
    # in biblioteca.
    # astfel incat selectarea din baza de date sa nu mai fie O(n) incepand cu a doua folosire ci porneste din __last_id.
    def updateBooks(library: Library):
        books = database.query(f"select * from books WHERE ID >= {LibraryController.__last_id}")
        for book in books:
            # print(book[0])
            id = book[0]
            LibraryController.__last_id = id
            
            author = book[1]
            title = book[2]
            status = book[3]
            publishDate = book[4]
            # parsare din string in obiect datetime
            parsed_date = datetime.datetime.strptime(publishDate, '%Y-%m-%d %H:%M:%S')
            #print(parsed_date)
            borrowedBy = int(book[5])
            noPages = book[6]

            tempBook = itemFactory.ItemFactory.createItem("book", id, author, title, status, parsed_date, borrowedBy=borrowedBy, noPages=noPages)

            existing_books = [existing_book.id for existing_book in library.getBooks()]
            
            if id not in existing_books:
                LibraryController.addBook(library, tempBook)

    def getBook(library: Library, id=0, name=None)-> libraryitems.Book:
        #return library.getBooks()[id]
        if name:
            for book in library.getBooks():
                if book.getTitle() == name:
                    return book
        
        return library.getBooks()[id]
    