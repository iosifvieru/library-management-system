import datetime
from flask import Flask, render_template, request, redirect, url_for, abort, flash, session
import libraryitems, itemFactory
import library as l
import database, random
import hashlib, user, string

app = Flask(__name__)
app.secret_key = 'pione4'
app.config['SESSION_PERMANENT'] = False

library = l.Library()
l.LibraryController.updateBooks(library)

listOfUsers = user.UserList()

sql = """
        DELETE from session WHERE id >= 1
    """
database.query(sql)

# MAIN PAGE
@app.route('/', methods=['GET','POST']) 
def mainPage():
    if not is_logged_in():
        return redirect('login')
    
    search = request.form.get('search_input')
    # print(search)

    books = library.getBooks()

    if search:
        tempList = list()
        for book in books:
            #if book.getTitle().lower() == search.lower() or book.getAuthor().lower() == search.lower():
            if str(search.lower()) in str(book.getTitle().lower()) or str(search.lower()) in str(book.getAuthor().lower()):
                tempList.append(book)

        books = tempList
            
    data = {
        'books': books,
        'adminLevel': session['adminLevel']
    }
    return render_template('index.html', **data)

# ADMIN
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


@app.route('/editBook', methods=['POST'])
def editBook():
    if not is_logged_in():
        return redirect('login')
    
    if request.method == 'POST':
        book_id = request.form.get('bookId')

        book_id = int(book_id)-1

        book = l.LibraryController.getBook(library, book_id)
        print(book)

        title = request.form.get('bookTitle')
        author = request.form.get('bookAuthor')
        publishDate = request.form.get('publishDate')
        borrowedBy = request.form.get('borrowedBy')
        noPages = request.form.get('noPages')

        sql = f"""
            UPDATE books SET author='{author}', title='{title}', publishDate='{publishDate}',
                            borrowedBy='{borrowedBy}', noPages='{noPages}' WHERE id = '{book.getId()}'
        """
        database.query(sql)
        
        # TO DO -> refresh object.
        book.refresh()

    return redirect('/')

@app.route('/edit', methods = ['POST', 'GET'])
def edit():
    if not is_logged_in():
        return redirect('login')
    
    if request.method == 'GET':
        book_id = int(request.args.get('bookId')) - 1
        book = l.LibraryController.getBook(library, book_id)

        data = {
            'book': book
        }
        return render_template('editBook.html', **data)


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
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        city = request.form.get('city')
        phoneNo = request.form.get('phoneNo')
        date = request.form.get('birthDate')

        parsed_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        encoded_password = encode_string(password)
        sql = f"""
            INSERT INTO users (username, password, email, firstName, lastName, 
                city, phoneNo, birthDate) VALUES ( 
                    '{username}', '{encoded_password}', '{email}', '{firstName}', 
                    '{lastName}', '{city}', '{phoneNo}', '{parsed_date}')"""

        database.query(sql)
        
        return redirect('/')
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    # verifica daca user ul este conectat deja.
    if is_logged_in():
        return redirect('/')

    if request.method == 'GET':
        return render_template('login.html')
    
    # codul de mai jos se executa daca request method este POST
    # adica logica de login propriu-zisa.
    username = request.form.get('username')
    password = request.form.get('password')
    encoded_password = encode_string(password)
    
    sql = f""" SELECT * FROM users WHERE username= '{username}'
        """
    result = database.query(sql)

    # restul = null inseamna ca nu s-a gasit utilizatorul in baza de date.
    if not result:
        return redirect('login')
        
    # ia primul set de date returnat de query.
    user = result[0]
    
    # daca parola != de parola din db -> redirect catre login.
    if user[2] != encoded_password:
        return redirect('login')

    id = user[0]
    username = user[1]
    first_name = user[3]
    last_name = user[4]
    city = user[5]
    phoneNo = user[6]
    email = user[7]
    birthDate = user[8]
    university = user[9]
    specialization = user[10]
    year = user[11]
    adminLevel = user[12]

    #session data
    session['user_id'] = user[0] # ID din Database.

    # generare cod session_id pt. validarea login-ului
    session_id = random.randint(1, 1000000)
    session['session_id'] = session_id
    session['adminLevel'] = adminLevel
    
    if not getSessionID(user[0]):
        sql = f"""
            INSERT INTO session (id, session_id) VALUES ('{int(session['user_id'])}', '{int(session['session_id'])}')
        """
        database.query(sql)
    else:
        sql = f"""
            UPDATE session SET session_id = '{session_id}' WHERE id = '{user[0]}'
        """
        database.query(sql)

    if birthDate:
        parsed_date = datetime.datetime.strptime(birthDate, '%Y-%m-%d %H:%M:%S')
        birthDate = parsed_date
    
    borrowedBooks = list()
    # to do
    for book in library.getBooks():
        if book.getBorrowedBy() == session['user_id']:
            borrowedBooks.append(book)

    tempUser = itemFactory.ItemFactory.createUser(id, first_name, last_name, city, phoneNo, email, birthDate, borrowedBooks, adminLevel, 
                                       university, specialization, year)

    listOfUsers.addUser(tempUser)


    return redirect('/')


@app.route('/logout')
def logout():
    #print("FROM LOGOUT: ")
    #print(listOfUsers.getUser(session['user_id']))

    if listOfUsers.getUser(session['user_id']):
        listOfUsers.removeUser(session['user_id'])
    
    deleteSession(int(session['user_id']))
    session.pop('user_id', None)

    # session.pop('adminLevel', None)
    return redirect('login')


# USER PAGE

@app.route('/profile')
def profile():
    if not is_logged_in():
        return redirect('/')
    
    #sql = f"""
    #    SELECT username, firstName, lastName, city, phoneNo, email, birthDate, university, specialization, year FROM users WHERE id= '{session['user_id']}'
    #"""

    #user_data = database.query(sql)

    #sql = f""" SELECT b.author, b.title FROM books b WHERE b.borrowedBy = '{session['user_id']}'
    #"""

    #books = database.query(sql)
    #print(books)

    #borrowedBooks = list()

    #for book in library.getBooks():
    #    if book.getBorrowedBy() == session['user_id']:
    #        borrowedBooks.append(book)
    user = listOfUsers.getUser(session['user_id'])
    books = user.displayCurrentBooks()

    profile_data = {
        'user': user,
        'books': books
    }

    #return render_template('profile.html', **profile_data)
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

    # update user class
    user = listOfUsers.getUser(book.getBorrowedBy())
    user.returnBook(book)

    # update book
    book.updateStatus(-1, book_id)

    return redirect('profile')

@app.route('/borrow', methods=['POST'])
def borrow_book():
    if not is_logged_in():
        return redirect('login')
    
    data = request.get_json()
    book_id = data.get('bookId')
    book_name = data.get('bookName')
    author = data.get('author')
    # print(data)

    book = l.LibraryController.getBook(library, int(book_id)-1)
    # print(book)
    # update user
    user = listOfUsers.getUser(session['user_id'])
    user.borrowBook(book)

    # update book
    book.updateStatus(session['user_id'], book_id)
    return redirect('/')


# ERROR HANDLE
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


def is_logged_in():
    return 'user_id' in session


# functie ce se apeleaza inainte de orice request http
# verifica daca sesiunea este valida.
# citeste din DB session_id si il compara cu session['session_id']
@app.before_request
def before_request():
    if 'user_id' in session:
        user_id = session['user_id']
        session_id_from_db = getSessionID(int(user_id))

        if session_id_from_db is None or session_id_from_db != int(session['session_id']):
            session.clear()
            return redirect(url_for('login'))


def deleteSession(id: int):
    sql = f"""
        DELETE from session WHERE id = '{id}'
    """
    database.query(sql)
    return None


def getSessionID(id: int):
    sql = f"""
        SELECT session_id from session WHERE id = '{id}'
    """
    session_id = database.query(sql)

    if session_id:
        return int(session_id[0][0])
    return None


def encode_string(string: str):
    key = "testkey"
    string += key

    hash = hashlib.sha256()
    hash.update(string.encode())
    encoded_pass = hash.hexdigest()
    return encoded_pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
