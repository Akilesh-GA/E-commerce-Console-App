import sqlite3 as s3

conn = s3.connect('e-commerce.db')

cur = conn.cursor()

cur.execute("SELECT * FROM products")
tables = cur.fetchall()

for table in tables:
    print(table)

conn.close()
