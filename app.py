from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key ="rahasia123hafizh2026"

def get_db():
    conn = sqlite3.connect("todo_web.db")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tugas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            nama TEXT,
            deskripsi TEXT DEFAULT ''
        )
    """)
    # tambah kolom user_id kalau belum ada
    try:
        conn.execute("ALTER TABLE tugas ADD COLUMN user_id INTEGER")
        conn.commit()
    except:
        pass
    conn.commit()
    return conn

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorate(*args, **kwargs):
        if "User_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorate
    
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    tugas = conn.execute("SELECT * FROM tugas WHERE user_id = ?", (session["user_id"],)).fetchall()
    conn.close()
    return render_template("index.html", tugas=tugas, username=session["username"])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        conn = get_db()
        try:
            conn.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except:
            conn.close()
            return render_template("register.html", error= "Username sudah dipakai!")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        user = conn.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        conn.close()
        print(f"User found: {user}")  # ← tambah ini
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("home"))
        return render_template("login.html", error="Username atau password salah!")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/tambah", methods=["POST"])
def tambah():
    if "user_id" not in session:
        return redirect(url_for("login"))
    nama = request.form["nama"]
    conn = get_db()
    conn.execute("INSERT INTO tugas (nama, user_id) VALUES (?, ?)", (nama, session["user_id"]))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route("/detail/<int:id>")
def detail(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    tugas = conn.execute("SELECT * FROM tugas WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("detail.html", tugas=tugas)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = get_db()          
    if request.method == "POST":
        nama = request.form["nama"]
        deskripsi = request.form["deskripsi"]
        conn.execute("UPDATE tugas SET nama = ?, deskripsi = ? WHERE id = ?", (nama, deskripsi, id))  
        conn.commit()
        conn.close()
        return redirect(url_for("detail", id=id))
    tugas = conn.execute("SELECT * FROM tugas WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", tugas=tugas)

@app.route("/hapus/<int:id>")
def hapus(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    conn.execute("DELETE FROM tugas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)