import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "ecommerce.db"

def setup():
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        city TEXT NOT NULL
    );

    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    );

    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    );

    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    );
    """)

    customers = [
        (1, "Maya Hassan", "Alexandria"),
        (2, "Omar Ali", "Cairo"),
        (3, "Nour Samir", "Giza"),
        (4, "Adam Youssef", "Alexandria"),
        (5, "Laila Mostafa", "Cairo"),
        (6, "Yassin Adel", "Mansoura"),
    ]
    products = [
        (1, "Wireless Mouse", "Electronics", 450.0),
        (2, "Mechanical Keyboard", "Electronics", 1800.0),
        (3, "Desk Lamp", "Home", 650.0),
        (4, "Office Chair", "Furniture", 3200.0),
        (5, "Notebook Set", "Stationery", 120.0),
        (6, "USB-C Hub", "Electronics", 950.0),
    ]
    orders = [
        (1, 1, "2026-10-01", "completed"),
        (2, 2, "2026-10-02", "completed"),
        (3, 1, "2026-10-04", "completed"),
        (4, 3, "2026-10-05", "cancelled"),
        (5, 4, "2026-10-09", "completed"),
        (6, 5, "2026-10-11", "pending"),
        (7, 2, "2026-10-13", "completed"),
        (8, 6, "2026-10-16", "completed"),
        (9, 3, "2026-10-18", "completed"),
        (10, 5, "2026-10-20", "completed"),
        (11, 4, "2026-10-22", "completed"),
        (12, 1, "2026-10-25", "completed"),
    ]
    items = [
        (1, 1, 1, 2, 450.0), (2, 1, 5, 3, 120.0),
        (3, 2, 2, 1, 1800.0), (4, 2, 6, 1, 950.0),
        (5, 3, 4, 1, 3200.0), (6, 3, 3, 2, 650.0),
        (7, 4, 3, 1, 650.0), (8, 5, 4, 1, 3200.0),
        (9, 5, 1, 1, 450.0), (10, 6, 5, 5, 120.0),
        (11, 7, 2, 1, 1800.0), (12, 7, 1, 1, 450.0),
        (13, 8, 6, 2, 950.0), (14, 8, 5, 2, 120.0),
        (15, 9, 3, 1, 650.0), (16, 9, 1, 2, 450.0),
        (17, 10, 4, 1, 3200.0), (18, 10, 5, 2, 120.0),
        (19, 11, 2, 1, 1800.0), (20, 11, 6, 1, 950.0),
        (21, 12, 1, 1, 450.0), (22, 12, 3, 1, 650.0),
    ]
    cur.executemany("INSERT INTO customers VALUES (?, ?, ?)", customers)
    cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)
    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders)
    cur.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?)", items)
    conn.commit()
    conn.close()
    print(f"Created sample database: {DB_PATH}")

if __name__ == "__main__":
    setup()
