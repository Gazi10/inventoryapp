import sqlite3

# c.execute("""CREATE TABLE inventory (
#             title text,
#             stock integer,
#             price real,
#             image text,
#             link text
#     )""")

def insert(data):
    conn = sqlite3.connect('inventory.db')
    v = (data[0],)
    c = conn.cursor()
    c.execute("SELECT * FROM inventory WHERE title == ?", v)
    if c.fetchone():
        c.execute("UPDATE inventory SET stock = stock + 1 WHERE title == ?", v)
    else:
        c.execute("INSERT INTO inventory VALUES (?, ?, ?, ?, ?)", ( data[0], data[1], data[2], data[3], data[4]))
    conn.commit()
    conn.close()


def select(value):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    v = (value,)
    c.execute("SELECT * FROM inventory WHERE title == ?", v)
    conn.commit()
    conn.close()


def delete(title):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    t = (title,)
    c.execute("SELECT stock FROM inventory WHERE title == ?", t)
    if c.fetchone()[0] == 1:
        c.execute("DELETE FROM inventory WHERE title == ?", t)
    else:
        c.execute("UPDATE inventory SET stock = stock - 1 WHERE title == ?", t)
    conn.commit()
    conn.close()

def show():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    conn.commit()
    conn.close()
    return items
