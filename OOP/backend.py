import sqlite3

class Database :
    """ This class for database """
    def __init__(self,db) :
        # MAke a connection. If file not exist, create a file
        self.conn = sqlite3.connect(db)
        # Make a cursor
        self.cur = self.conn.cursor()
        # SQL Code
        self.cur.execute("CREATE TABLE IF NOT EXISTS bookshop (id INTEGER PRIMARY KEY, title TEXT, author TEXT, yearofbook INTEGER, isbn INTEGER)")
        # commit
        self.conn.commit()

    def insert(self,title, author, yearofbook, isbn):
        # SQL Code
        self.cur.execute("INSERT INTO bookshop VALUES (NULL,?,?,?,?)",(title, author, yearofbook, isbn))
        # commit
        self.conn.commit()

    def view(self):
        # SQL Code
        self.cur.execute("SELECT * FROM bookshop")
        rows = self.cur.fetchall()
        return rows

    def search(self,title="", author="", yearofbook="", isbn=""):
        # SQL Code
        self.cur.execute("SELECT * FROM bookshop WHERE title=? OR author=? OR yearofbook=? OR isbn=?",(title, author, yearofbook, isbn))
        rows = self.cur.fetchall()
        return rows

    def delete(self,id) :
        # SQL Code
        self.cur.execute("DELETE FROM bookshop WHERE id=?",(id,))
        # commit
        self.conn.commit()

    def update(self,id,title, author, yearofbook, isbn):
        # SQL Code
        self.cur.execute("UPDATE bookshop SET title=?, author=?, yearofbook=?, isbn=? WHERE id=?",(title, author, yearofbook, isbn,id))
        # commit
        self.conn.commit()
        
    def __del__(self) :
        # Close connection
        self.conn.close()

