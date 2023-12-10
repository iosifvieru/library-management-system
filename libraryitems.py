from abc import ABC, abstractmethod
import datetime, database, itemFactory


class LibraryItem(ABC):
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def updateStatus(self):
        pass



# self.status -> deprecated

# borrowedBy -> deprecated, va fi folosit ca foreign key pentru libraryID. din libraries

class Book(LibraryItem):
    def __init__(self, id: int, author: str, name: str,
                 status: bool, publishDate: datetime, borrowedBy: int, noPages: int):
        self.id = id
        self.author = author
        self.name = name
        self.status = status
        self.publishDate = publishDate
        self.borrowedBy = borrowedBy
        self.noPages = noPages
        self.quantity = 0

        self.libraryID = borrowedBy
        
        sql = f"""
            SELECT name from libraries WHERE libraryID = '{self.libraryID}'
        """
        result = database.query(sql)

        if result:
            result = result[0]
            self.libraryName = result[0]
            
            # print(self.libraryName)
            
        # quantity



        sql = f"""
            SELECT quantity from book_quantities WHERE id = '{self.id}'
        """

        result = database.query(sql)
        if result:
            result = result[0]
            self.quantity = result[0]

        # print(self.quantity)

    def updateQuantity(self, quantity: int):
        sql = f"""
            SELECT quantity FROM book_quantities WHERE id = '{self.id}'
        """
        result = database.query(sql)

        if not result:
            sql = f"""
                INSERT INTO book_quantities (id, quantity) VALUES ('{self.id}', '{quantity}')
            """
            result = database.query(sql)

        sql = f"""
            UPDATE book_quantities SET quantity='{quantity}' WHERE id = '{self.id}'
        """
        database.query(sql)

    def display(self):
        borrowed = "neimprumutat"
        if self.status is True:
            borrowed = f"imprumutat lui {self.borrowedBy}"

        string = f"id: {self.id}, author: {self.author}, name: {self.name}, " \
                 f"status: {borrowed}, publishDate: {self.publishDate}, noPages: {self.noPages}"

        return string

    def updateStatus(self, borrowedBy: int, bookID: int):
        # to do: de modificat self.borrowedBy
        #if borrowedBy >= -1:
        self.borrowedBy = borrowedBy
            # qur
        sql = None
        if self.borrowedBy >= -1:
            self.status = True
            sql = f'UPDATE books SET borrowedBy = {self.borrowedBy}, status = True WHERE id = {bookID}'
        else:
            self.status = False
            sql = f'UPDATE books SET borrowedBy = {self.borrowedBy}, status = False WHERE id = {bookID}'

        database.query(sql)

    def getQuantity(self):
        sql = f"""
            SELECT quantity FROM book_quantities WHERE id='{self.id}'
        """
        quantity = database.query(sql)
        quantity = quantity[0][0]

        return quantity

    def refresh(self):

        sql = f"""
            SELECT * FROM books where id = '{self.id}'
        """
        result = database.query(sql)
        result = result[0]

        self.id = result[0]
        self.author = result[1]
        self.name = result[2]
        self.status = result[3]
        self.borrowedBy = result[5]
        self.noPages = result[6]

        self.setLibraryID(self.borrowedBy)

        # quantity refresh
        sql = f"""
            SELECT quantity from book_quantities where id = '{self.id}'

        """
        result = database.query(sql)
        result = result[0]

        self.quantity = result[0]

        # TO DO: 
        #date = result[4]
        #parsed_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        #if self.publishDate != parsed_date:
        #    self.publishDate = parsed_date

    def createCopy(self):
        object = itemFactory.ItemFactory.createItem("book", self.id, self.author, self.name, self.status, self.publishDate,
                                                    self.borrowedBy, self.noPages)
        return object

    def __str__(self):
        return self.display()
    
    def __repr__(self) -> str:
        return self.display()
    
    def getId(self):
        return self.id
    
    def getBorrowedBy(self):
        return self.borrowedBy
    
    def getAuthor(self):
        return self.author
    
    def getTitle(self):
        return self.name
    
    def setTitle(self, title):
        self.name = title
    
    def setAuthor(self, author):
        self.author = author

    def setLibraryID(self, id):
        self.libraryID = id

    def getLibraryID(self):
        return self.libraryID
    
    def getLibraryName(self):
        return self.libraryName