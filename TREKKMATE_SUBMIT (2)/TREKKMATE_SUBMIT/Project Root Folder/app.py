# app.py
# TREKKMATE - Trek Management System
# Nishant Girhepunje 24F3000141
# This is the main file that handles all the routes

from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = "trekkmate_secret_123"

DB_NAME = "trekkmate.db"

# function to get database connection
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# creating tables if not exists
def create_tables():
    conn = get_db()
    cur = conn.cursor()

    # users table - stores all users (admin, staff, user)
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

    # treks table - stores all treks
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

    # bookings table - stores all bookings
    cur.execute("""CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL, trek_id INTEGER NOT NULL,
        booking_date TEXT DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Booked',
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (trek_id) REFERENCES treks(id)
    )""")

    # create admin if not exists
    cur.execute("SELECT * FROM users WHERE role='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username,password,full_name,email,phone,role,status) VALUES ('Nishant','Nishant2418','System Admin','admin@trekkmate.com','9999999999','admin','active')")
        print("admin created!")

    conn.commit()
    conn.close()


# decorator to check if user is logged in
def login_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return check


# decorator to check if user is admin
def admin_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first", "warning")
            return redirect(url_for("login"))
        if session.get("role") != "admin":
            flash("Admin access required", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return check


# decorator to check if user is staff
def staff_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first", "warning")
            return redirect(url_for("login"))
        if session.get("role") != "staff":
            flash("Staff access required", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return check


# decorator to check if user is regular user
def user_required(f):
    @wraps(f)
    def check(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first", "warning")
            return redirect(url_for("login"))
        if session.get("role") != "user":
            flash("User access required", "danger")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return check


# ==================== PUBLIC ROUTES ====================

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        conn.close()
        if user:
            if user["status"] == "blacklisted":
                flash("Your account has been blacklisted. Contact admin.", "danger")
                return redirect(url_for("login"))
            # save user info in session
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["full_name"] = user["full_name"]
            flash("Login successful!", "success")
            print("user logged in:", username, "as", user["role"])
            # redirect based on role
            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            elif user["role"] == "staff":
                return redirect(url_for("staff_dashboard"))
            else:
                return redirect(url_for("user_dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        role = request.form["role"]
        # only staff and user can register
        if role not in ["staff", "user"]:
            flash("Invalid role", "danger")
            return redirect(url_for("register"))
        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username,password,full_name,email,phone,role) VALUES (?,?,?,?,?,?)",
                        (username, password, full_name, email, phone, role))
            conn.commit()
            print("new registration:", username, "role:", role)
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists. Try another.", "danger")
        finally:
            conn.close()
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("home"))


# ==================== ADMIN ROUTES ====================

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    conn = get_db()
    # get counts for dashboard stats
    total_treks = conn.execute("SELECT COUNT(*) as cnt FROM treks").fetchone()["cnt"]
    total_users = conn.execute("SELECT COUNT(*) as cnt FROM users WHERE role='user'").fetchone()["cnt"]
    total_staff = conn.execute("SELECT COUNT(*) as cnt FROM users WHERE role='staff'").fetchone()["cnt"]
    total_bookings = conn.execute("SELECT COUNT(*) as cnt FROM bookings").fetchone()["cnt"]
    pending_staff = conn.execute("SELECT COUNT(*) as cnt FROM users WHERE role='staff' AND status='pending'").fetchone()["cnt"]
    print("admin dashboard - treks:", total_treks, "users:", total_users)
    conn.close()
    return render_template("admin/dashboard.html", total_treks=total_treks, total_users=total_users,
                           total_staff=total_staff, total_bookings=total_bookings, pending_staff=pending_staff)


@app.route("/admin/treks")
@admin_required
def admin_treks():
    conn = get_db()
    treks = conn.execute("SELECT t.*, u.full_name as staff_name FROM treks t LEFT JOIN users u ON t.staff_id = u.id ORDER BY t.id DESC").fetchall()
    conn.close()
    return render_template("admin/treks.html", treks=treks)


@app.route("/admin/treks/add", methods=["GET", "POST"])
@admin_required
def admin_add_trek():
    if request.method == "POST":
        name = request.form["name"].strip()
        location = request.form["location"].strip()
        difficulty = request.form["difficulty"]
        duration = int(request.form["duration"])
        total_slots = int(request.form["total_slots"])
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        description = request.form["description"].strip()
        price = float(request.form["price"])
        conn = get_db()
        conn.execute("INSERT INTO treks (name,location,difficulty,duration,total_slots,available_slots,start_date,end_date,description,price) VALUES (?,?,?,?,?,?,?,?,?,?)",
                     (name, location, difficulty, duration, total_slots, total_slots, start_date, end_date, description, price))
        conn.commit()
        conn.close()
        print("trek added:", name)
        flash("Trek added successfully!", "success")
        return redirect(url_for("admin_treks"))
    return render_template("admin/add_trek.html")


@app.route("/admin/treks/edit/<int:trek_id>", methods=["GET", "POST"])
@admin_required
def admin_edit_trek(trek_id):
    conn = get_db()
    trek = conn.execute("SELECT * FROM treks WHERE id=?", (trek_id,)).fetchone()
    if not trek:
        flash("Trek not found", "danger")
        return redirect(url_for("admin_treks"))
    if request.method == "POST":
        name = request.form["name"].strip()
        location = request.form["location"].strip()
        difficulty = request.form["difficulty"]
        duration = int(request.form["duration"])
        total_slots = int(request.form["total_slots"])
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        description = request.form["description"].strip()
        price = float(request.form["price"])
        # calculate available slots
        booked = conn.execute("SELECT COUNT(*) as cnt FROM bookings WHERE trek_id=? AND status='Booked'", (trek_id,)).fetchone()["cnt"]
        available = total_slots - booked
        if available < 0:
            available = 0
        conn.execute("UPDATE treks SET name=?,location=?,difficulty=?,duration=?,total_slots=?,available_slots=?,start_date=?,end_date=?,description=?,price=? WHERE id=?",
                     (name, location, difficulty, duration, total_slots, available, start_date, end_date, description, price, trek_id))
        conn.commit()
        conn.close()
        flash("Trek updated successfully!", "success")
        return redirect(url_for("admin_treks"))
    conn.close()
    return render_template("admin/edit_trek.html", trek=trek)


@app.route("/admin/treks/delete/<int:trek_id>")
@admin_required
def admin_delete_trek(trek_id):
    conn = get_db()
    # cancel all bookings for this trek first
    conn.execute("UPDATE bookings SET status='Cancelled' WHERE trek_id=?", (trek_id,))
    conn.execute("DELETE FROM treks WHERE id=?", (trek_id,))
    conn.commit()
    conn.close()
    print("trek deleted:", trek_id)
    flash("Trek deleted successfully!", "success")
    return redirect(url_for("admin_treks"))


@app.route("/admin/staff")
@admin_required
def admin_staff():
    conn = get_db()
    staff = conn.execute("SELECT * FROM users WHERE role='staff' ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin/staff.html", staff_list=staff)


@app.route("/admin/staff/add", methods=["GET", "POST"])
@admin_required
def admin_add_staff():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        conn = get_db()
        try:
            conn.execute("INSERT INTO users (username,password,full_name,email,phone,role,status) VALUES (?,?,?,?,?,'staff','active')",
                        (username, password, full_name, email, phone))
            conn.commit()
            print("admin added staff:", username)
            flash("Staff added successfully!", "success")
        except sqlite3.IntegrityError:
            flash("Username already exists!", "danger")
        finally:
            conn.close()
        return redirect(url_for("admin_staff"))
    return render_template("admin/add_staff.html")


@app.route("/admin/staff/delete/<int:user_id>")
@admin_required
def admin_delete_staff(user_id):
    conn = get_db()
    # remove staff from treks first
    conn.execute("UPDATE treks SET staff_id=NULL WHERE staff_id=?", (user_id,))
    conn.execute("DELETE FROM users WHERE id=? AND role='staff'", (user_id,))
    conn.commit()
    conn.close()
    print("staff deleted:", user_id)
    flash("Staff deleted!", "warning")
    return redirect(url_for("admin_staff"))


@app.route("/admin/staff/approve/<int:user_id>")
@admin_required
def admin_approve_staff(user_id):
    conn = get_db()
    conn.execute("UPDATE users SET status='active' WHERE id=? AND role='staff'", (user_id,))
    conn.commit()
    conn.close()
    print("staff approved:", user_id)
    flash("Staff approved successfully!", "success")
    return redirect(url_for("admin_staff"))


@app.route("/admin/staff/blacklist/<int:user_id>")
@admin_required
def admin_blacklist_staff(user_id):
    conn = get_db()
    conn.execute("UPDATE users SET status='blacklisted' WHERE id=? AND role='staff'", (user_id,))
    conn.commit()
    conn.close()
    flash("Staff blacklisted!", "warning")
    return redirect(url_for("admin_staff"))


@app.route("/admin/staff/activate/<int:user_id>")
@admin_required
def admin_activate_staff(user_id):
    conn = get_db()
    conn.execute("UPDATE users SET status='active' WHERE id=? AND role='staff'", (user_id,))
    conn.commit()
    conn.close()
    flash("Staff activated!", "success")
    return redirect(url_for("admin_staff"))


@app.route("/admin/assign_staff/<int:trek_id>", methods=["GET", "POST"])
@admin_required
def admin_assign_staff(trek_id):
    conn = get_db()
    trek = conn.execute("SELECT * FROM treks WHERE id=?", (trek_id,)).fetchone()
    active_staff = conn.execute("SELECT * FROM users WHERE role='staff' AND status='active'").fetchall()
    if request.method == "POST":
        staff_id = request.form["staff_id"]
        if staff_id == "none":
            staff_id = None
        else:
            staff_id = int(staff_id)
        conn.execute("UPDATE treks SET staff_id=? WHERE id=?", (staff_id, trek_id))
        conn.commit()
        conn.close()
        flash("Staff assigned successfully!", "success")
        return redirect(url_for("admin_treks"))
    conn.close()
    return render_template("admin/assign_staff.html", trek=trek, staff_list=active_staff)


@app.route("/admin/users")
@admin_required
def admin_users():
    conn = get_db()
    users = conn.execute("SELECT * FROM users WHERE role='user' ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin/users.html", users=users)


@app.route("/admin/users/blacklist/<int:user_id>")
@admin_required
def admin_blacklist_user(user_id):
    conn = get_db()
    conn.execute("UPDATE users SET status='blacklisted' WHERE id=? AND role='user'", (user_id,))
    conn.commit()
    conn.close()
    flash("User blacklisted!", "warning")
    return redirect(url_for("admin_users"))


@app.route("/admin/users/delete/<int:user_id>")
@admin_required
def admin_delete_user(user_id):
    conn = get_db()
    # cancel all bookings and restore slots
    conn.execute("UPDATE bookings SET status='Cancelled' WHERE user_id=? AND status='Booked'", (user_id,))
    bookings = conn.execute("SELECT trek_id FROM bookings WHERE user_id=? AND status='Cancelled'", (user_id,)).fetchall()
    for b in bookings:
        conn.execute("UPDATE treks SET available_slots = available_slots + 1 WHERE id=?", (b["trek_id"],))
    conn.execute("DELETE FROM users WHERE id=? AND role='user'", (user_id,))
    conn.commit()
    conn.close()
    print("user deleted:", user_id)
    flash("User deleted!", "warning")
    return redirect(url_for("admin_users"))


@app.route("/admin/users/activate/<int:user_id>")
@admin_required
def admin_activate_user(user_id):
    conn = get_db()
    conn.execute("UPDATE users SET status='active' WHERE id=? AND role='user'", (user_id,))
    conn.commit()
    conn.close()
    flash("User activated!", "success")
    return redirect(url_for("admin_users"))


@app.route("/admin/bookings")
@admin_required
def admin_bookings():
    conn = get_db()
    bookings = conn.execute("SELECT b.*, t.name as trek_name, u.full_name as user_name FROM bookings b JOIN treks t ON b.trek_id = t.id JOIN users u ON b.user_id = u.id ORDER BY b.id DESC").fetchall()
    conn.close()
    return render_template("admin/bookings.html", bookings=bookings)


@app.route("/admin/search", methods=["GET", "POST"])
@admin_required
def admin_search():
    results = []
    query = ""
    search_type = ""
    if request.method == "POST":
        query = request.form["query"].strip()
        search_type = request.form["search_type"]
        conn = get_db()
        if search_type == "treks":
            results = conn.execute("SELECT * FROM treks WHERE name LIKE ? OR location LIKE ? OR id=?", (f"%{query}%", f"%{query}%", query if query.isdigit() else -1)).fetchall()
        elif search_type == "users":
            results = conn.execute("SELECT * FROM users WHERE role='user' AND (full_name LIKE ? OR username LIKE ? OR id=?)", (f"%{query}%", f"%{query}%", query if query.isdigit() else -1)).fetchall()
        elif search_type == "staff":
            results = conn.execute("SELECT * FROM users WHERE role='staff' AND (full_name LIKE ? OR username LIKE ? OR id=?)", (f"%{query}%", f"%{query}%", query if query.isdigit() else -1)).fetchall()
        conn.close()
        print("search:", query, "in", search_type, "->", len(results), "results")
    return render_template("admin/search.html", results=results, query=query, search_type=search_type)


# ==================== STAFF ROUTES ====================

@app.route("/staff/dashboard")
@staff_required
def staff_dashboard():
    conn = get_db()
    staff_id = session["user_id"]
    # get treks assigned to this staff with booked count
    assigned_treks = conn.execute("SELECT t.*, (SELECT COUNT(*) FROM bookings WHERE trek_id=t.id AND status='Booked') as booked_count FROM treks t WHERE t.staff_id=? ORDER BY t.id DESC", (staff_id,)).fetchall()
    conn.close()
    return render_template("staff/dashboard.html", treks=assigned_treks)


@app.route("/staff/trek/<int:trek_id>", methods=["GET", "POST"])
@staff_required
def staff_trek_detail(trek_id):
    conn = get_db()
    staff_id = session["user_id"]
    trek = conn.execute("SELECT * FROM treks WHERE id=? AND staff_id=?", (trek_id, staff_id)).fetchone()
    if not trek:
        flash("You are not assigned to this trek", "danger")
        return redirect(url_for("staff_dashboard"))
    if request.method == "POST":
        action = request.form.get("action")
        if action == "update_slots":
            new_slots = int(request.form["available_slots"])
            conn.execute("UPDATE treks SET available_slots=? WHERE id=?", (new_slots, trek_id))
            conn.commit()
            print("slots updated:", new_slots)
            flash("Slots updated!", "success")
        elif action == "update_status":
            new_status = request.form["trek_status"]
            conn.execute("UPDATE treks SET status=? WHERE id=?", (new_status, trek_id))
            conn.commit()
            print("status changed to:", new_status)
            flash("Status updated!", "success")
        # refresh trek data
        trek = conn.execute("SELECT * FROM treks WHERE id=? AND staff_id=?", (trek_id, staff_id)).fetchone()
    # get participants
    participants = conn.execute("SELECT b.*, u.full_name, u.email, u.phone FROM bookings b JOIN users u ON b.user_id = u.id WHERE b.trek_id=? AND b.status='Booked'", (trek_id,)).fetchall()
    conn.close()
    return render_template("staff/trek_detail.html", trek=trek, participants=participants)


# ==================== USER ROUTES ====================

@app.route("/user/dashboard")
@user_required
def user_dashboard():
    conn = get_db()
    user_id = session["user_id"]
    # get available treks
    available_treks = conn.execute("SELECT t.*, u.full_name as staff_name FROM treks t LEFT JOIN users u ON t.staff_id = u.id WHERE t.status='Open' AND t.available_slots > 0 ORDER BY t.start_date ASC").fetchall()
    # get user's bookings
    my_bookings = conn.execute("SELECT b.*, t.name as trek_name, t.location, t.difficulty, t.start_date FROM bookings b JOIN treks t ON b.trek_id = t.id WHERE b.user_id=? ORDER BY b.id DESC", (user_id,)).fetchall()
    conn.close()
    return render_template("user/dashboard.html", available_treks=available_treks, my_bookings=my_bookings)


@app.route("/user/treks")
@user_required
def user_treks():
    conn = get_db()
    difficulty = request.args.get("difficulty", "")
    location = request.args.get("location", "")
    # build query based on filters
    query = "SELECT t.*, u.full_name as staff_name FROM treks t LEFT JOIN users u ON t.staff_id = u.id WHERE t.status='Open' AND t.available_slots > 0"
    params = []
    if difficulty:
        query += " AND t.difficulty=?"
        params.append(difficulty)
    if location:
        query += " AND t.location LIKE ?"
        params.append(f"%{location}%")
    query += " ORDER BY t.start_date ASC"
    treks = conn.execute(query, params).fetchall()
    conn.close()
    return render_template("user/treks.html", treks=treks, difficulty=difficulty, location=location)


@app.route("/user/book/<int:trek_id>")
@user_required
def user_book_trek(trek_id):
    conn = get_db()
    user_id = session["user_id"]
    trek = conn.execute("SELECT * FROM treks WHERE id=?", (trek_id,)).fetchone()
    if not trek:
        flash("Trek not found", "danger")
        return redirect(url_for("user_treks"))
    # check if already booked
    existing = conn.execute("SELECT * FROM bookings WHERE user_id=? AND trek_id=? AND status='Booked'", (user_id, trek_id)).fetchone()
    if existing:
        flash("You already have a booking for this trek!", "warning")
        return redirect(url_for("user_dashboard"))
    # check if slots available
    if trek["available_slots"] <= 0:
        flash("No slots available!", "danger")
        return redirect(url_for("user_treks"))
    # check if trek is open
    if trek["status"] != "Open":
        flash("Trek is not open for booking!", "danger")
        return redirect(url_for("user_treks"))
    # create booking
    conn.execute("INSERT INTO bookings (user_id, trek_id) VALUES (?, ?)", (user_id, trek_id))
    conn.execute("UPDATE treks SET available_slots = available_slots - 1 WHERE id=?", (trek_id,))
    conn.commit()
    conn.close()
    print("booking created - user:", user_id, "trek:", trek_id)
    flash("Trek booked successfully!", "success")
    return redirect(url_for("user_dashboard"))


@app.route("/user/cancel/<int:booking_id>")
@user_required
def user_cancel_booking(booking_id):
    conn = get_db()
    user_id = session["user_id"]
    booking = conn.execute("SELECT * FROM bookings WHERE id=? AND user_id=?", (booking_id, user_id)).fetchone()
    if not booking:
        flash("Booking not found", "danger")
        return redirect(url_for("user_dashboard"))
    # cancel booking and restore slot
    conn.execute("UPDATE bookings SET status='Cancelled' WHERE id=?", (booking_id,))
    conn.execute("UPDATE treks SET available_slots = available_slots + 1 WHERE id=?", (booking["trek_id"],))
    conn.commit()
    conn.close()
    print("booking cancelled:", booking_id)
    flash("Booking cancelled!", "info")
    return redirect(url_for("user_dashboard"))


@app.route("/user/profile", methods=["GET", "POST"])
@user_required
def user_profile():
    conn = get_db()
    user_id = session["user_id"]
    user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        password = request.form["password"].strip()
        # update password only if provided
        if password:
            conn.execute("UPDATE users SET full_name=?, email=?, phone=?, password=? WHERE id=?", (full_name, email, phone, password, user_id))
        else:
            conn.execute("UPDATE users SET full_name=?, email=?, phone=? WHERE id=?", (full_name, email, phone, user_id))
        conn.commit()
        session["full_name"] = full_name
        flash("Profile updated!", "success")
        user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return render_template("user/profile.html", user=user)

@app.route("/user/history")
@user_required
def user_history():
    conn = get_db()
    user_id = session["user_id"]
    bookings = conn.execute("SELECT b.*, t.name as trek_name, t.location, t.difficulty, t.start_date, t.end_date FROM bookings b JOIN treks t ON b.trek_id = t.id WHERE b.user_id=? ORDER BY b.id DESC", (user_id,)).fetchall()
    conn.close()
    return render_template("user/history.html", bookings=bookings)

# main - run the app
if __name__ == "__main__":
    create_tables()
    app.run(debug=True, port=5000)