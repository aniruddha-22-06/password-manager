import json
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
    site = input("Enter website: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    encrypted_password = cipher.encrypt(password.encode()).decode()

    data = load_data()
    data[site] = {
        "username": username,
        "password": encrypted_password
    }

    save_data(data)
    print("Password saved successfully.")


def view_passwords():
    data = load_data()

    for site, info in data.items():
        decrypted = cipher.decrypt(info["password"].encode()).decode()
        print(f"\nSite: {site}")
        print(f"Username: {info['username']}")
        print(f"Password: {decrypted}")


def delete_password():
    site = input("Enter site to delete: ")
    data = load_data()

    if site in data:
        del data[site]
        save_data(data)
        print("Deleted successfully.")
    else:
        print("Site not found.")


def main():
    while True:
        print("\n1. Add Password")
        print("2. View Passwords")
        print("3. Delete Password")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            delete_password()
        elif choice == "4":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
