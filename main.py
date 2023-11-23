import datetime
from flask import Flask, render_template, request, redirect, url_for, abort, flash, session
import libraryitems, itemFactory
import library as l
import database
import hashlib, user

app = Flask(__name__)
app.secret_key = 'pione4'
app.config['SESSION_PERMANENT'] = False

library = l.Library()
l.LibraryController.updateBooks(library)

@app.route('/') 
def mainPage():
    if not is_logged_in():
        return redirect('login')
    
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


@app.route('/borrow', methods=['POST'])
def borrow_book():
    if not is_logged_in():
        return redirect('login')
    
    data = request.get_json()
    book_id = data.get('bookId')
    book_name = data.get('bookName')
    author = data.get('author')
    print(data)
    book = l.LibraryController.getBook(library, int(book_id)-1)
    print(book)
    
    book.updateStatus(session['user_id'], book_id)
    return redirect('/')


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


# LOGIN REGISTER SYSTEM

@app.route('/register', methods=['POST', 'GET'])
def register():
    if is_logged_in():
        return redirect('/')

    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        encoded_password = encode_string(password)
        sql = f"""
            INSERT INTO users (username, password, email) VALUES ( '{username}', '{encoded_password}', '{email}' )"""

        database.query(sql)
        
        return redirect('/')

@app.route('/profile')
def profile():
    if not is_logged_in():
        return redirect('/')
    
    sql = f"""
        SELECT username, firstName, lastName, city, phoneNo, email, birthDate, university, specialization, year FROM users WHERE id= '{session['user_id']}'
    """

    user_data = database.query(sql)

    #sql = f""" SELECT b.author, b.title FROM books b WHERE b.borrowedBy = '{session['user_id']}'
    #"""

    #books = database.query(sql)
    #print(books)

    borrowedBooks = list()

    for book in library.getBooks():
        if book.getBorrowedBy() == session['user_id']:
            borrowedBooks.append(book)

    profile_data = {
        'user': user_data[0],
        'books': borrowedBooks
    }

    return render_template('profile.html', **profile_data)


@app.route('/return', methods=['POST'])
def return_book():
    data = request.get_json()
    book_id = data.get('bookId')
    book_name = data.get('bookName')
    author = data.get('author')
    print(data)
    book = l.LibraryController.getBook(library, int(book_id)-1)
    print(book)

    book.updateStatus(-1, book_id)

    return redirect('profile')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if is_logged_in():
        return redirect('/')

    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')

    encoded_password = encode_string(password)
    sql = f""" SELECT * FROM users WHERE username= '{username}'
        """

    result = database.query(sql)
    if not result:
        return redirect('login')
        
    user = result[0]
    if user[2] != encoded_password:
        return redirect('login')
    
    session['user_id'] = user[0] # ID din Database.

    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('login')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404

def is_logged_in():
    return 'user_id' in session


def encode_string(string: str):
    hash = hashlib.sha256()
    hash.update(string.encode())
    encoded_pass = hash.hexdigest()
    return encoded_pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
