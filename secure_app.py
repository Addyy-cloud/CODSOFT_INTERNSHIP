import sqlite3
import hashlib
import os
import hmac

DATABASE = "secure_users.db"


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)

    password_hash = hashlib.scrypt(
        password.encode(),
        salt=salt,
        n=16384,
        r=8,
        p=1
    )

    return salt.hex(), password_hash.hex()


def verify_password(password, stored_salt, stored_hash):
    salt = bytes.fromhex(stored_salt)

    password_hash = hashlib.scrypt(
        password.encode(),
        salt=salt,
        n=16384,
        r=8,
        p=1
    )

    return hmac.compare_digest(
        password_hash.hex(),
        stored_hash
    )


def setup_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)

    username = "aditya"
    password = "password123"

    salt, password_hash = hash_password(password)

    cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password_hash, salt)
        VALUES (?, ?, ?)
    """, (username, password_hash, salt))

    connection.commit()
    connection.close()


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Secure: parameterized SQL query
    cursor.execute(
        "SELECT password_hash, salt FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    connection.close()

    if user:
        stored_hash, stored_salt = user

        if verify_password(password, stored_salt, stored_hash):
            print("\nLogin successful!")
            return

    # Generic message prevents unnecessary information disclosure
    print("\nInvalid username or password.")


def main():
    setup_database()

    print("===================================")
    print("        SECURE LOGIN SYSTEM")
    print("===================================")

    login()


if __name__ == "__main__":
    main() 