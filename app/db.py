import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer TEXT NOT NULL,
    total_cents INTEGER NOT NULL CHECK (total_cents >= 0)
);
"""


def connect(path):
    # Declared types are parsed, so INTEGER and friends come back as Python values.
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn


def init(conn):
    conn.executescript(SCHEMA)
    conn.commit()


def add_order(conn, customer, total_cents):
    cur = conn.execute(
        "INSERT INTO orders (customer, total_cents) VALUES (?, ?)", (customer, total_cents)
    )
    conn.commit()
    return cur.lastrowid


def get_order(conn, order_id):
    return conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()


def list_orders(conn):
    return conn.execute("SELECT * FROM orders ORDER BY id").fetchall()
