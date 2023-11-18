import libraryitems


class Library:
    def __init__(self):
        self.items = list()

    def print(self):
        result_string = '\n'.join(book.__str__() for book in self.items)
        return result_string

    def getBooks(self):
        return self.items


class LibraryController:
    @staticmethod
    def addBook(library: Library, book: libraryitems.Book):
        library.items.append(book)
