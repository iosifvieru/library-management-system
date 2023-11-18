import datetime
from flask import Flask, render_template, request, redirect, url_for, abort
import libraryitems, itemFactory
import library as l
import database

app = Flask(__name__)

library = l.Library()
l.LibraryController.updateBooks(library)

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
        #tempItem = itemFactory.ItemFactory.createItem(item_type, id, author, title, False, date, -1, noPages)
        #if tempItem is None:
        #    abort(404)
        
        #l.LibraryController.addBook(library, tempItem)

        sql = f"""
            INSERT INTO books (author, title, status, publishDate, borrowedBy, noPages)
            VALUES ('{author}', '{title}', '{False}', '{date}', '{-1}', {noPages});
        """
        database.query(sql)

        l.LibraryController.updateBooks(library)
        return redirect(url_for('addBook'))



@app.route('/sql', methods=['POST', 'GET'])
def sql_admin():
    if request.method == 'GET':
        return render_template('sql.html')
    else:
        sql = request.form.get('sqlInput')
        
        result = database.query(sql)
        print(result)
        
        return redirect('sql')
    #return render_template('sql.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
