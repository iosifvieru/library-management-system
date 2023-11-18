from abc import ABC, abstractmethod
import datetime


class LibraryItem(ABC):
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def updateStatus(self):
        pass


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

    def display(self):
        borrowed = "neimprumutat"
        if self.status is True:
            borrowed = f"imprumutat lui {self.borrowedBy}"

        string = f"id: {self.id}, author: {self.author}, name: {self.name}, " \
                 f"status: {borrowed}, publishDate: {self.publishDate}, noPages: {self.noPages}"

        return string

    def updateStatus(self):
        self.status = not self.status

    def __str__(self):
        return self.display()
