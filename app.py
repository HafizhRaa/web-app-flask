from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("todo_web.db")
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tugas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            deskripsi TEXT DEFAULT ''
        )
    """)
    conn.commit()
    return conn

@app.route("/")
def home():
    conn = get_db()
    tugas = conn.execute("SELECT * FROM tugas").fetchall()
    conn.close()
    return render_template("index.html", tugas=tugas)

@app.route("/tambah", methods=["POST"])
def tambah():
    nama = request.form["nama"]
    conn = get_db()
    conn.execute("INSERT INTO tugas (nama) VALUES (?)", (nama,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route("/detail/<int:id>")
def detail(id):
    conn = get_db()
    tugas = conn.execute("SELECT * FROM tugas WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("detail.html", tugas=tugas)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()          # ← tambah ()
    if request.method == "POST":
        nama = request.form["nama"]
        deskripsi = request.form["deskripsi"]
        conn.execute("UPDATE tugas SET nama = ?, deskripsi = ? WHERE id = ?", (nama, deskripsi, id))  # ← id kecil
        conn.commit()
        conn.close()
        return redirect(url_for("detail", id=id))
    tugas = conn.execute("SELECT * FROM tugas WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", tugas=tugas)

@app.route("/hapus/<int:id>")
def hapus(id):
    conn = get_db()
    conn.execute("DELETE FROM tugas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tugas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            deskripsi TEXT DEFAULT ''
        )
""")
    conn.commit()
    conn.close()
    app.run(debug=True)