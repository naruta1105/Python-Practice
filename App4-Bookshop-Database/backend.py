import sqlite3

def create_table() :
    # MAke a connection. If file not exist, create a file
    conn = sqlite3.connect("book.db")
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("CREATE TABLE IF NOT EXISTS bookshop (id INTEGER PRIMARY KEY, title TEXT, author TEXT, yearofbook INTEGER, isbn INTEGER)")
    # commit
    conn.commit()
    # Close connection
    conn.close()

def insert(title, author, yearofbook, isbn):
    # MAke a connection. If file not exist, create a file
    conn = sqlite3.connect("book.db")
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("INSERT INTO bookshop VALUES (NULL,?,?,?,?)",(title, author, yearofbook, isbn))
    # commit
    conn.commit()
    # Close connection
    conn.close()

def view():
    conn = sqlite3.connect("book.db")
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("SELECT * FROM bookshop")
    rows = cur.fetchall()
    # Close connection
    conn.close()
    return rows

def search(title="", author="", yearofbook="", isbn=""):
    conn = sqlite3.connect("book.db")
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("SELECT * FROM bookshop WHERE title=? OR author=? OR yearofbook=? OR isbn=?",(title, author, yearofbook, isbn))
    rows = cur.fetchall()
    # Close connection
    conn.close()
    return rows

def delete(id) :
    conn = sqlite3.connect("book.db")
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("DELETE FROM bookshop WHERE id=?",(id,))
    # commit
    conn.commit()
    # Close connection
    conn.close()

def update(id,title, author, yearofbook, isbn):
    conn = sqlite3.connect("book.db")
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("UPDATE bookshop SET title=?, author=?, yearofbook=?, isbn=? WHERE id=?",(title, author, yearofbook, isbn,id))
    # commit
    conn.commit()
    # Close connection
    conn.close()

create_table()