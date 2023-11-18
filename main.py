import datetime
from flask import Flask, render_template, request, redirect, url_for, abort
import libraryitems, itemFactory
import library as l
import database

app = Flask(__name__)

library = l.Library()

books = database.query("select * from books")
#print(books)


for book in books:
    id = book[0]
    author = book[1]
    title = book[2]
    status = book[3]
    publishDate = book[4]
    # 
    parsed_date = datetime.datetime.strptime(publishDate, '%Y-%m-%d %H:%M:%S')
    print(parsed_date)

    borrowedBy = book[5]
    noPages = book[6]
    tempBook = itemFactory.ItemFactory.createItem("book", id, author, title, status, parsed_date, borrowedBy, noPages)
    l.LibraryController.addBook(library, tempBook)


@app.route('/')
def mainPage():
    return render_template('index.html', books=library.getBooks())


@app.route('/addBook', methods=['POST', 'GET'])
def addBook():
    if request.method == 'GET':
        return render_template('addBook.html')
    else:
        item_type = request.form.get('item_type')
        author = request.form.get('author')
        title = request.form.get('title')
        date = datetime.datetime(day=1, month=11, year=int(request.form.get('date')))
        noPages = int(request.form.get('noPages'))
        #tempBook = libraryitems.Book(4, author, title, False, datetime.datetime(day=1, month=11, year=int(date)), -1, noPages)
        tempItem = itemFactory.ItemFactory.createItem(item_type, id, author, title, False, date, -1, noPages)
        if tempItem is None:
            abort(404)
        
        l.LibraryController.addBook(library, tempItem)

        sql = f"""
            INSERT INTO books (author, title, status, publishDate, borrowedBy, noPages)
            VALUES ('{author}', '{title}', '{False}', '{date}', '{-1}', {noPages});
        """
        
        database.query(sql)

        # to do: de adaugat in baza de date.
        return redirect(url_for('addBook'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
