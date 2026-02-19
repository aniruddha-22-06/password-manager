# 🔐 Flask Password Manager

A simple and secure **Password Manager Web Application** built using **Python and Flask**.
It allows users to store, generate, and manage their passwords safely using encryption.

---

## 🚀 Features

* User login system
* Add and store passwords securely
* View saved credentials
* Password generation feature
* Encrypted password storage
* Simple and clean web interface

---

## 🛠️ Technologies Used

* Python 3
* Flask
* HTML5
* CSS3
* SQLite (passwords.db)
* Cryptography (for encryption)

---

## 📂 Project Structure

```
password manager/
│
├── app.py                 # Main Flask application
├── generate_key.py        # Encryption key generator
├── passwords.db           # SQLite database
├── data.json              # Additional stored data
├── key.key                # Encryption key
├── master.key             # Master key file
├── requirements.txt       # Project dependencies
├── LICENSE
├── README.md
│
├── static/
│   └── style.css          # Stylesheet
│
├── templates/
│   ├── login.html         # Login page
│   ├── add.html           # Add password page
│   └── passwords.html     # View passwords page
│
├── screenshots/
│   ├── home.png
│   ├── add.png
│   └── view.png
│
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd password-manager
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate encryption key (first time only)

```bash
python generate_key.py
```

### 5. Run the application

```bash
python app.py
```

Open browser and go to:

```
http://127.0.0.1:5000
```

---

## 📸 Screenshots

Add your screenshots inside a `screenshots` folder and update the names if needed.

Example:

```
screenshots/
   home.png
   add.png
   view.png
```

---

## 🔐 Security Note

* Passwords are encrypted before storage.
* Keep the `key.key` and `master.key` files safe.
* Do not share encryption keys publicly.

---

## 🎯 Future Improvements

* User registration system
* Password strength indicator
* Dark mode
* Cloud backup
* Two-factor authentication

---

## 👨‍💻 Author

**Aniruddha**
Computer Science Student
Learning Python, Web Development, and Data Structures

---

## 📜 License

This project is licensed under the terms of the LICENSE file.
