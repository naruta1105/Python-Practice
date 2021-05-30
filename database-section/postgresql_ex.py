# PostgreSQL
import psycopg2

database = "dbname='dtbase01' user='postgres' password='postgres123' host='localhost' port='5432'"

def create_table() :
    # MAke a connection. If file not exist, create a file
    conn = psycopg2.connect(database)
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("CREATE TABLE IF NOT EXISTS store (item TEXT, quantity INTEGER, price REAL)")
    # commit
    conn.commit()
    # Close connection
    conn.close()

def insert(item,quality,price):
    # MAke a connection. If file not exist, create a file
    conn = psycopg2.connect(database)
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("INSERT INTO store VALUES (%s,%s,%s)",(item,quality,price))
    # commit
    conn.commit()
    # Close connection
    conn.close()

def view():
    conn = psycopg2.connect(database)
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("SELECT * FROM store")
    rows = cur.fetchall()
    # Close connection
    conn.close()
    return rows

def delete(item):
    conn = psycopg2.connect(database)
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("DELETE FROM store WHERE item=%s",(item,))
    # commit
    conn.commit()
    # Close connection
    conn.close()

def update(item,quantity,price):
    conn = psycopg2.connect(database)
    # Make a cursor
    cur = conn.cursor()
    # SQL Code
    cur.execute("UPDATE store SET quantity=%s, price=%s WHERE item=%s",(quantity,price,item))
    # commit
    conn.commit()
    # Close connection
    conn.close()

create_table()
update("Apple",20,15)
print(view())