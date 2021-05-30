import sqlite3

def create_table() :
    # MAke a connection. If file not exist, create a file
    conn = sqlite3.connect("lite.db")
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("CREATE TABLE IF NOT EXISTS store (item TEXT, quantiny INTEGER, price REAL)")
    # commit
    conn.commit()
    # Close connection
    conn.close()

def insert(item,quality,price):
    # MAke a connection. If file not exist, create a file
    conn = sqlite3.connect("lite.db")
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("INSERT INTO store VALUES (?,?,?)",(item,quality,price))
    # commit
    conn.commit()
    # Close connection
    conn.close()

def view():
    conn = sqlite3.connect("lite.db")
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("SELECT * FROM store")
    rows = cur.fetchall()
    # Close connection
    conn.close()
    return rows

def delete(item):
    conn = sqlite3.connect("lite.db")
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("DELETE FROM store WHERE item=?",(item,))
    # commit
    conn.commit()
    # Close connection
    conn.close()

def update(item,quantity,price):
    conn = sqlite3.connect("lite.db")
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("UPDATE store SET quantiny=?, price=? WHERE item=?",(quantity,price,item))
    # commit
    conn.commit()
    # Close connection
    conn.close()

update("Wine Glass",5,9.5)
print(view())