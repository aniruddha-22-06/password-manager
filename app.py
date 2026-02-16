from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta
import sqlite3
import os
from cryptography.fernet import Fernet
import bcrypt

app = Flask(__name__)

# ---------- Session Security ----------
app.secret_key = "supersecretkey123"
app.permanent_session_lifetime = timedelta(minutes=5)

# ---------- Password Hashing ----------
MASTER_FILE = "master.key"

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def load_master():
    if not os.path.exists(MASTER_FILE):
        default_password = "admin"
        hashed = hash_password(default_password)
        with open(MASTER_FILE, "wb") as f:
            f.write(hashed)

    with open(MASTER_FILE, "rb") as f:
        return f.read()

master_hash = load_master()

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
        entered = request.form["password"]
        if check_password(entered, master_hash):
            session["user"] = "logged_in"
            session.permanent = True
            return redirect(url_for("add"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect(url_for("login"))

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
    if "user" not in session:
        return redirect(url_for("login"))

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
    if "user" not in session:
        return redirect(url_for("login"))

    cursor.execute("DELETE FROM passwords WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for("view_passwords"))


if __name__ == "__main__":
    app.run(debug=False)
