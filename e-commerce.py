import sqlite3 as s3

conn = s3.connect('e-commerce.db')

cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS users''')

cur.execute('''CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(25) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE CHECK (email LIKE '%_@_%_.com'),
    age INTEGER NOT NULL CHECK (age >= 18),
    address VARCHAR(50) NOT NULL,
    phone VARCHAR(10) NOT NULL CHECK (phone GLOB '[0-9]*' AND LENGTH(phone) = 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')

cur.execute('''DROP TABLE IF EXISTS products''')

cur.execute('''CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name VARCHAR(25) NOT NULL,
    price INTEGER NOT NULL CHECK (price > 0),
    stock INTEGER CHECK (stock > 0),
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
)''')

cur.execute('''DROP TABLE IF EXISTS orders''')

cur.execute('''CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_date DATETIME NOT NULL,
    order_status VARCHAR(25) NOT NULL,
    shipping_address VARCHAR,
    total_amount INTEGER NOT NULL CHECK (total_amount > 0),
    payment_status VARCHAR,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)''')

cur.execute('''DROP TABLE IF EXISTS reviews''')

cur.execute('''CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    reviewer_name VARCHAR(25) NOT NULL,
    reviewer_mail VARCHAR(50) NOT NULL UNIQUE CHECK (reviewer_mail LIKE '%_@_%_.com'),
    rating INTEGER NOT NULL CHECK (rating > 0 AND rating <= 10),
    comment TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)''')

cur.execute('''DROP TABLE IF EXISTS payments''')

cur.execute('''CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    payment_date DATETIME NOT NULL,
    amount INTEGER NOT NULL,
    payment_method VARCHAR(25),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)''')

def add_products():
    
    print("\nEnter Details to Add Products\n")

    product_name = input("Enter Product Name: ")
    price = int(input("Enter Price: "))
    stock = int(input("Enter Number of stocks: "))

    cur.execute('''INSERT INTO products (product_name, price, stock) VALUES (?, ?, ?)''',
                (product_name, price, stock))
    
    print("\nproducts added successfully ! ")
    print("THANK YOU !\n")

    conn.commit()

def drop_products():

    print("\nEnter Details to delete Product\n")

    product_id = int(input("Enter Product ID: "))

    cur.execute('''DELETE FROM products WHERE product_id = ?''', (product_id,))
    
    print("\nProduct deleted successfully ! ")

    conn.commit()


def view_products():
    
    print("\nAvailable Products in Store\n")

    cur.execute('''SELECT * FROM products''')
    products_table = cur.fetchall()

    for record in products_table:
        print(record)
    
    conn.commit()

def order_products():
    
    print("\nEnter Details to Order products\n")

    user_id = int(input("Enter user id : "))
    order_date = input("Enter Ordered Date (YYYY-MM-DD) : ")
    order_status = input("Enter Order Status : ")
    shipping_address = input("Enter Address : ")
    total_amount = int(input("Enter Total Amount to Pay : "))

    cur.execute('''INSERT INTO orders (user_id,order_date,order_status,shipping_address,total_amount) VALUES (?,?,?,?,?) ''',
    (user_id,order_date,order_status,shipping_address,total_amount))

    print("\nProduct Ordered Succssfully ! ")
    print("Thank You for Orders\n")

    conn.commit()


def review_products():
    
    print("\nEnter Your Review of Product\n")

    user_id = int(input("Enter your user id : "))
    product_id = int(input("Enter your product id : "))
    reviewer_name = input("Enter your Name : ")
    reviewer_mail = input("Enter your e-mail address : ")
    rating = int(input("Enter Rating (1-10) : "))
    comment = input("Enter Comments : ")
    review_date = input("Enter Date of review (YYYY-MM-DD) : ")

    cur.execute('''INSERT INTO reviews (user_id,product_id,reviewer_name,reviewer_mail,rating,comment,review_date) VALUES
                (?,?,?,?,?,?,?)''',(user_id,product_id,reviewer_name,reviewer_mail,rating,comment,review_date))

    print("\nThank You for your product Review\n")

    conn.commit()

def update_stocks():
    
    print("\nEnter Detials to update stocks \n")

    product_id = int(input("Enter Product id :"))
    stock = int(input("Enter Stocks : "))

    cur.execute('''UPDATE products SET stock = ? WHERE product_id = ? ''',
    (stock,product_id))

    print("\nStock Updated successfully ! \n")
    
    conn.commit()


def payment():
    
    print("\nEnter Payment Details \n")

    user_id = int(input("Enter user id : "))
    order_id = int(input("Enter Order id : "))
    payment_date = input("Enter Payment Date (YYYY-MM-DD) : ")
    amount = int(input("Enter Amount to pay : "))
    payment_method = input("Enter Payment Method (UPI,Cash On Delivery,Credit Card) : ")

    cur.execute('''INSERT INTO payments (user_id,order_id,payment_date,amount,payment_method) VALUES
    (?,?,?,?,?)''',(user_id,order_id,payment_date,amount,payment_method))

    print("\nPayment Successfull !")
    print("Thank you for your Orders \n")

    conn.commit()



def menu():
    while True:
        print("\n" + "="*40)
        print("      E-COMMERCE MANAGEMENT MENU ")
        print("="*40)
        print("1 -> Add Products")
        print("2 -> Delete Products")
        print("3 -> View Products")
        print("4 -> Order Products")
        print("5 -> Give Product Review")
        print("6 -> Update stocks ")
        print("7 -> Payment")
        print("0 -> Exit Menu")
        print("="*40 + "\n")

        val = int(input("Enter option: "))

        if val <= 0:
            break
        elif val == 1:
            add_products()
        elif val == 2:
            drop_products()
        elif val == 3:
            view_products()
        elif val == 4:
            order_products()
        elif val == 5:
            review_products()
        elif val == 6:
            update_stocks()
        elif val == 7:
            payment()
        else:
            print("\nInvalid Input")
            print("Please enter a number within (1-7)")

menu()

conn.close()