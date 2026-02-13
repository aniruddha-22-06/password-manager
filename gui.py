import json
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# Load key
with open("key.key", "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)
DATA_FILE = "data.json"


def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except:
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)


def add_password():
    site = entry_site.get()
    username = entry_user.get()
    password = entry_pass.get()

    if not site or not username or not password:
        messagebox.showerror("Error", "All fields required")
        return

    encrypted = cipher.encrypt(password.encode()).decode()
    data = load_data()
    data[site] = {"username": username, "password": encrypted}
    save_data(data)

    messagebox.showinfo("Success", "Password saved")
    entry_site.delete(0, tk.END)
    entry_user.delete(0, tk.END)
    entry_pass.delete(0, tk.END)


def view_passwords():
    data = load_data()
    result = ""

    for site, info in data.items():
        decrypted = cipher.decrypt(info["password"].encode()).decode()
        result += f"{site} | {info['username']} | {decrypted}\n"

    if result == "":
        result = "No passwords saved."

    messagebox.showinfo("Saved Passwords", result)


def delete_password():
    site = entry_site.get()
    data = load_data()

    if site in data:
        del data[site]
        save_data(data)
        messagebox.showinfo("Deleted", "Password deleted")
    else:
        messagebox.showerror("Error", "Site not found")


# GUI window
root = tk.Tk()
root.title("Password Manager")
root.geometry("350x250")

tk.Label(root, text="Website").pack()
entry_site = tk.Entry(root, width=30)
entry_site.pack()

tk.Label(root, text="Username").pack()
entry_user = tk.Entry(root, width=30)
entry_user.pack()

tk.Label(root, text="Password").pack()
entry_pass = tk.Entry(root, width=30, show="*")
entry_pass.pack()

tk.Button(root, text="Save Password", command=add_password).pack(pady=5)
tk.Button(root, text="View Passwords", command=view_passwords).pack(pady=5)
tk.Button(root, text="Delete Password", command=delete_password).pack(pady=5)

root.mainloop()
