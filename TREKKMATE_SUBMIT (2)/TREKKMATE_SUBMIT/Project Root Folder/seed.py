# adds demo data to database

from database import get_db, create_tables
def seed_data():
    conn = get_db()
    cur = conn.cursor()

    count = cur.execute("SELECT COUNT(*) as cnt FROM users WHERE role='staff'").fetchone()["cnt"]
    if count > 0:
        print("data already exists, skipping...")
        conn.close()
        return

    # staff
    staff_data = [
        ("aadi", "aadi2418", "Aadi Kumar", "aadi@gmail.com", "9876543210", "staff", "active"),
        ("priya_guide", "priya123", "Priya Patel", "priya@gmail.com", "9876543211", "staff", "active"),
        ("amit_guide", "amit123", "Amit Kumar", "amit@gmail.com", "9876543212", "staff", "active"),
        ("neha_guide", "neha123", "Neha Gupta", "neha@gmail.com", "9876543213", "staff", "pending"),
    ]
    for s in staff_data:
        cur.execute("INSERT INTO users (username,password,full_name,email,phone,role,status) VALUES (?,?,?,?,?,?,?)", s)
    print("added 4 staff")

    # users
    user_data = [
        ("rishabh", "rishabh123", "Rishabh Singh", "rishabh@gmail.com", "9123456780", "user", "active"),
        ("sneha", "sneha123", "Sneha Desai", "sneha@gmail.com", "9123456781", "user", "active"),
        ("karan", "karan123", "Karan Mehta", "karan@gmail.com", "9123456782", "user", "active"),
        ("ankita", "ankita123", "Ankita Rao", "ankita@gmail.com", "9123456783", "user", "active"),
        ("varun", "varun123", "Varun Nair", "varun@gmail.com", "9123456784", "user", "active"),
    ]
    for u in user_data:
        cur.execute("INSERT INTO users (username,password,full_name,email,phone,role,status) VALUES (?,?,?,?,?,?,?)", u)
    print("added 5 users")

    # treks
    trek_data = [
        ("Kedarkantha Trek", "Uttarakhand", "Moderate", 6, 20, 20, 2, "Open", "2026-01-15", "2026-01-21", "Snow trek to Kedarkantha peak.", 8500),
        ("Triund Trek", "Dharamshala", "Easy", 2, 25, 25, 3, "Open", "2026-02-10", "2026-02-12", "Short weekend trek near McLeodGanj.", 2500),
        ("Valley of Flowers", "Uttarakhand", "Moderate", 5, 15, 15, 2, "Open", "2026-07-01", "2026-07-06", "Trek through beautiful meadows.", 7000),
        ("Chadar Trek", "Ladakh", "Hard", 9, 10, 10, 3, "Pending", "2026-01-20", "2026-01-29", "Frozen river trek in Ladakh.", 15000),
        ("Rohtang Pass Trek", "Himachal Pradesh", "Moderate", 4, 18, 18, None, "Open", "2026-06-15", "2026-06-19", "Scenic mountain views.", 6500),
        ("Hampta Pass Trek", "Himachal Pradesh", "Hard", 5, 12, 12, None, "Pending", "2026-09-01", "2026-09-06", "Cross-valley trek.", 9000),
        ("Brahmatal Trek", "Uttarakhand", "Easy", 4, 20, 20, 3, "Open", "2026-03-05", "2026-03-09", "Winter trek with frozen lake.", 5500),
        ("Sandakphu Trek", "West Bengal", "Hard", 7, 15, 15, 2, "Open", "2026-11-10", "2026-11-17", "Kanchenjunga views.", 11000),
    ]
    for t in trek_data:
        cur.execute("INSERT INTO treks (name,location,difficulty,duration,total_slots,available_slots,staff_id,status,start_date,end_date,description,price) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", t)
    print("added 8 treks")

    # bookings
    booking_data = [
        (6, 1, "Booked"), (7, 2, "Booked"), (8, 1, "Booked"),
        (9, 3, "Booked"), (10, 2, "Booked"), (6, 7, "Booked"),
    ]
    for b in booking_data:
        cur.execute("INSERT INTO bookings (user_id, trek_id, status) VALUES (?, ?, ?)", b)

    cur.execute("UPDATE treks SET available_slots = total_slots - (SELECT COUNT(*) FROM bookings WHERE bookings.trek_id = treks.id AND bookings.status = 'Booked')")
    print("added 6 bookings")

    conn.commit()
    conn.close()
    print("\ndone! data added")
    print("\nlogin details:")
    print("-" * 35)
    print("admin:   Nishant / Nishant2418")
    print("staff:   aadi / aadi2418")
    print("user:    rishabh / rishabh123")


if __name__ == "__main__":
    create_tables()
    seed_data()
