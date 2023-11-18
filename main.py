import datetime
from flask import Flask, render_template
import libraryitems
import library as l

app = Flask(__name__)

# citite din DB
book = libraryitems.Book(1, "Feodor Dostoievski", "Fratii Karamazov", True,
                         datetime.datetime(day=1, month=11, year=1880), -1, 840)
book2 = libraryitems.Book(2, "Albert Camus", "Strainul", True, datetime.datetime(year=1942, month=1, day=1), 222, 185)
book3 = libraryitems.Book(3, "Franz Kafka", "Metamorfoza", True, datetime.datetime(year=1915, month=1, day=1), 222, 344)

library = l.Library()
l.LibraryController.addBook(library, book)
l.LibraryController.addBook(library, book2)
l.LibraryController.addBook(library, book3)


@app.route('/')
def hello_world():
    return render_template('index.html', books=library.getBooks())


@app.route('/addBook')
def addBook():
    return render_template('addBook.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
