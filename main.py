import json
import hashlib
import re
import os

FILE_NAME = "users.json"
MAX_ATTEMPTS = 3

# ---------- File Handling ----------

def load_users():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return json.load(file)

def save_users(users):
    with open(FILE_NAME, "w") as file:
        json.dump(users, file, indent=4)

# ---------- Security ----------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- Validation ----------

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def is_strong_password(password):
    return len(password) >= 6

# ---------- Register ----------

def register():
    users = load_users()

    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    if not is_valid_email(email):
        print("Invalid email!")
        return

    if not is_strong_password(password):
        print("Weak password!")
        return

    for user in users:
        if user["username"] == username or user["email"] == email:
            print("User already exists!")
            return

    role = input("Enter role (admin/user): ").lower()
    if role not in ["admin", "user"]:
        role = "user"

    users.append({
        "username": username,
        "email": email,
        "password": hash_password(password),
        "role": role,
        "attempts": 0
    })

    save_users(users)
    print("Registered successfully!")

# ---------- Login ----------

def login():
    users = load_users()
    username = input("Enter username/email: ").strip()

    for user in users:
        if user["username"] == username or user["email"] == username:

            if user["attempts"] >= MAX_ATTEMPTS:
                print("Account locked!")
                return

            password = input("Enter password: ")
            if user["password"] == hash_password(password):
                print(f"Welcome {user['username']} ({user['role']})")
                user["attempts"] = 0
                save_users(users)

                # Role-based message
                if user["role"] == "admin":
                    print("Admin Access Granted")
                else:
                    print("User Access")

                return
            else:
                user["attempts"] += 1
                save_users(users)
                print(f"Wrong password ({user['attempts']}/{MAX_ATTEMPTS})")
                return

    print("User not found!")

# ---------- Password Reset ----------

def reset_password():
    users = load_users()
    email = input("Enter your email: ").strip()

    for user in users:
        if user["email"] == email:
            new_password = input("Enter new password: ").strip()

            if not is_strong_password(new_password):
                print("Weak password!")
                return

            user["password"] = hash_password(new_password)
            user["attempts"] = 0  # unlock account
            save_users(users)

            print("Password reset successful!")
            return

    print("Email not found!")

# ---------- Delete Account ----------

def delete_account():
    users = load_users()

    username = input("Enter username: ")
    password = input("Enter password: ")

    for user in users:
        if user["username"] == username and user["password"] == hash_password(password):
            users.remove(user)
            save_users(users)
            print("Account deleted!")
            return

    print(" Invalid credentials!")

# ---------- Admin Unlock ----------

def unlock_account():
    users = load_users()
    username = input("Enter username to unlock: ")

    for user in users:
        if user["username"] == username:
            user["attempts"] = 0
            save_users(users)
            print("Account unlocked!")
            return

    print("User not found!")

# ---------- Menu ----------

def main():
    while True:
        print("\n===== AUTH SYSTEM =====")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. Delete Account")
        print("5. Unlock Account (Admin)")
        print("6. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            reset_password()
        elif choice == "4":
            delete_account()
        elif choice == "5":
            unlock_account()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

# ---------- Run ----------

if __name__ == "__main__":
    main()