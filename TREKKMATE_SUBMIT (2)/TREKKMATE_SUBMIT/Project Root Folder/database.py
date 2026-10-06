import sqlite3

DB_NAME = "trekkmate.db"
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT, phone TEXT,
        role TEXT NOT NULL,
        status TEXT DEFAULT 'active',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS treks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, location TEXT NOT NULL,
        difficulty TEXT NOT NULL, duration INTEGER NOT NULL,
        total_slots INTEGER NOT NULL, available_slots INTEGER NOT NULL,
        staff_id INTEGER, status TEXT DEFAULT 'Pending',
        start_date TEXT, end_date TEXT, description TEXT,
        price REAL DEFAULT 0, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (staff_id) REFERENCES users(id)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL, trek_id INTEGER NOT NULL,
        booking_date TEXT DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Booked',
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (trek_id) REFERENCES treks(id)
    )""")

    cur.execute("SELECT * FROM users WHERE role='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username,password,full_name,email,phone,role,status) VALUES ('Nishant','Nishant2418','System Admin','admin@trekkmate.com','9999999999','admin','active')")
        print("admin created!")

    conn.commit()
    conn.close()
