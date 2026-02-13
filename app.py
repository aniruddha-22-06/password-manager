import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os
from cryptography.fernet import Fernet
import re

# ---------------- Encryption Setup ----------------
KEY_FILE = "key.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    return open(KEY_FILE, "rb").read()

key = load_key()
cipher = Fernet(key)

# ---------------- Database Setup ----------------
conn = sqlite3.connect("passwords.db")
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

# ---------------- Strength Meter ----------------
def check_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*]", password):
        score += 1

    if score == 1:
        return "Weak"
    elif score == 2:
        return "Medium"
    elif score >= 3:
        return "Strong"
    return "Very Weak"

# ---------------- App ----------------
class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Manager")
        self.root.geometry("900x520")
        self.root.configure(bg="#1e1e2f")

        self.show_login()

    # ---------- LOGIN SCREEN ----------
    def show_login(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack(expand=True)

        tk.Label(frame, text="Login", font=("Arial", 26, "bold"),
                 fg="white", bg="#1e1e2f").pack(pady=20)

        tk.Label(frame, text="Master Password",
                 fg="white", bg="#1e1e2f").pack()

        self.master_entry = tk.Entry(frame, show="*", width=30)
        self.master_entry.pack(pady=10)

        tk.Button(frame, text="Login",
                  command=self.check_login,
                  bg="#4CAF50", fg="white",
                  width=20, height=2).pack(pady=10)

    def check_login(self):
        if self.master_entry.get() == "admin":
            self.show_main()
        else:
            messagebox.showerror("Error", "Wrong master password")

    # ---------- MAIN SCREEN ----------
    def show_main(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#1e1e2f")
        main_frame.pack(fill="both", expand=True)

        # LEFT PANEL
        left = tk.Frame(main_frame, bg="#2b2b45", width=350)
        left.pack(side="left", fill="y")

        tk.Label(left, text="Password Manager",
                 font=("Arial", 20, "bold"),
                 fg="white", bg="#2b2b45").pack(pady=30)

        form = tk.Frame(left, bg="#2b2b45")
        form.pack(pady=20)

        tk.Label(form, text="Site", fg="white",
                 bg="#2b2b45").grid(row=0, column=0, pady=8, sticky="w")

        self.site_entry = tk.Entry(form, width=25)
        self.site_entry.grid(row=0, column=1, padx=10)

        tk.Label(form, text="Username", fg="white",
                 bg="#2b2b45").grid(row=1, column=0, pady=8, sticky="w")

        self.user_entry = tk.Entry(form, width=25)
        self.user_entry.grid(row=1, column=1, padx=10)

        tk.Label(form, text="Password", fg="white",
                 bg="#2b2b45").grid(row=2, column=0, pady=8, sticky="w")

        self.pass_entry = tk.Entry(form, show="*", width=25)
        self.pass_entry.grid(row=2, column=1, padx=10)
        self.pass_entry.bind("<KeyRelease>", self.update_strength)

        self.strength_label = tk.Label(left, text="Strength: ",
                                       fg="white", bg="#2b2b45",
                                       font=("Arial", 12))
        self.strength_label.pack(pady=10)

        tk.Button(left, text="Save Password",
                  command=self.save_password,
                  bg="#4CAF50", fg="white",
                  width=20, height=2).pack(pady=10)

        tk.Button(left, text="View Stored Passwords",
                  command=self.show_passwords_page,
                  bg="#2196F3", fg="white",
                  width=20, height=2).pack(pady=5)

        # RIGHT PANEL
        right = tk.Frame(main_frame, bg="#1e1e2f")
        right.pack(side="left", fill="both", expand=True)

        tk.Label(right,
                 text="Secure Storage\nEncrypted with Fernet",
                 font=("Arial", 22, "bold"),
                 fg="#4CAF50",
                 bg="#1e1e2f",
                 justify="center").pack(expand=True)

    # ---------- PASSWORD LIST PAGE ----------
    def show_passwords_page(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        top = tk.Frame(frame, bg="#1e1e2f")
        top.pack(fill="x")

        tk.Label(top, text="Stored Passwords",
                 font=("Arial", 18, "bold"),
                 fg="white", bg="#1e1e2f").pack(side="left")

        tk.Button(top, text="Back",
                  command=self.show_main,
                  bg="#888", fg="white").pack(side="right")

        # Search bar
        search_frame = tk.Frame(frame, bg="#1e1e2f")
        search_frame.pack(fill="x", pady=10)

        tk.Label(search_frame, text="Search:",
                 fg="white", bg="#1e1e2f").pack(side="left")

        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=10)

        tk.Button(search_frame, text="Search",
                  command=self.search_passwords,
                  bg="#2196F3", fg="white").pack(side="left")

        tk.Button(search_frame, text="Show All",
                  command=self.load_passwords,
                  bg="#4CAF50", fg="white").pack(side="left", padx=5)

        # Table
        self.tree = ttk.Treeview(frame,
                                 columns=("Site", "Username", "Password"),
                                 show="headings", height=12)

        self.tree.heading("Site", text="Site")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")

        self.tree.pack(fill="both", expand=True, pady=10)

        tk.Button(frame, text="Delete Selected",
                  command=self.delete_password,
                  bg="#f44336", fg="white",
                  width=20).pack(pady=5)

        self.load_passwords()

    # ---------- FUNCTIONS ----------
    def save_password(self):
        site = self.site_entry.get()
        username = self.user_entry.get()
        password = self.pass_entry.get()

        if not site or not username or not password:
            messagebox.showwarning("Warning", "Fill all fields")
            return

        encrypted = cipher.encrypt(password.encode()).decode()

        cursor.execute("INSERT INTO passwords (site, username, password) VALUES (?, ?, ?)",
                       (site, username, encrypted))
        conn.commit()

        messagebox.showinfo("Success", "Password saved")

    def load_passwords(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor.execute("SELECT id, site, username, password FROM passwords")
        for row in cursor.fetchall():
            decrypted = cipher.decrypt(row[3].encode()).decode()
            self.tree.insert("", "end", iid=row[0],
                             values=(row[1], row[2], decrypted))

    def search_passwords(self):
        query = self.search_entry.get()

        for row in self.tree.get_children():
            self.tree.delete(row)

        cursor.execute("""
        SELECT id, site, username, password FROM passwords
        WHERE site LIKE ? OR username LIKE ?
        """, (f"%{query}%", f"%{query}%"))

        for row in cursor.fetchall():
            decrypted = cipher.decrypt(row[3].encode()).decode()
            self.tree.insert("", "end", iid=row[0],
                             values=(row[1], row[2], decrypted))

    def delete_password(self):
        selected = self.tree.selection()
        if not selected:
            return

        for item in selected:
            cursor.execute("DELETE FROM passwords WHERE id=?",
                           (item,))
        conn.commit()
        self.load_passwords()

    def update_strength(self, event=None):
        password = self.pass_entry.get()
        strength = check_strength(password)
        self.strength_label.config(text=f"Strength: {strength}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ---------------- Run App ----------------
root = tk.Tk()
app = PasswordManager(root)
root.mainloop()
