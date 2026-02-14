from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from cryptography.fernet import Fernet

app = Flask(__name__)

# ---------- Encryption ----------
KEY_FILE = "key.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)

    with open(KEY_FILE, "rb") as f:
        return f.read()

key = load_key()
cipher = Fernet(key)

# ---------- Database ----------
conn = sqlite3.connect("passwords.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site TEXT,
    username TEXT,
    password TEXT
)
""")
conn.commit()

# ---------- Routes ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == "admin":
            return redirect(url_for("add"))
    return render_template("login.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    message = ""
    if request.method == "POST":
        site = request.form["site"]
        username = request.form["username"]
        password = request.form["password"]

        encrypted = cipher.encrypt(password.encode()).decode()

        cursor.execute(
            "INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)",
            (site, username, encrypted)
        )
        conn.commit()

        message = "Password saved successfully!"

    return render_template("add.html", message=message)


@app.route("/passwords")
def view_passwords():
    cursor.execute("SELECT id, site, username, password FROM passwords")
    rows = cursor.fetchall()

    data = []
    for row in rows:
        decrypted = cipher.decrypt(row[3].encode()).decode()
        data.append({
            "id": row[0],
            "site": row[1],
            "username": row[2],
            "password": decrypted
        })

    return render_template("passwords.html", passwords=data)



@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute("DELETE FROM passwords WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for("view_passwords"))


if __name__ == "__main__":
    app.run(debug=False)
