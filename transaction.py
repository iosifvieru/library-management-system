import user
import database

class Transaction:
    def borrowBook(book, user):
        bookQuantity = book.getQuantity()

        if(bookQuantity <= 0):
            pass
        
        tempObject = book.createCopy()

        user.borrowBook(tempObject)

        # sql
        sql = f"""
            INSERT INTO borrowedBooks (user_id, book_id) VALUES ('{user.getID()}', '{tempObject.getId()}')
        """
        database.query(sql)

        book.updateQuantity(bookQuantity - 1)

        # ..

    def returnBook(book, user):
        # delete din db
        # increment la cantitate in db
        sql = f"""
            DELETE FROM borrowedBooks WHERE user_id = '{user.getID()}' and book_id = '{book.getId()}'
        """
        database.query(sql)
        
        bookQuantity = book.getQuantity()
        book.updateQuantity(bookQuantity + 1)