import sqlite3

DATABASE = "users.db"

# Vulnerability 1: Hardcoded credentials
ADMIN_PASSWORD = "admin123"


def setup_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            password TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO users VALUES ('aditya', 'password123')"
    )

    connection.commit()
    connection.close()


def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Vulnerability 2: SQL Injection
    query = (
        "SELECT * FROM users WHERE username = '"
        + username
        + "' AND password = '"
        + password
        + "'"
    )

    try:
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            print("\nLogin successful!")
        else:
            print("\nInvalid username or password.")

    except Exception as error:
        # Vulnerability 3: Excessive error information
        print("\nDatabase error:", error)

    connection.close()


def main():
    setup_database()

    print("===================================")
    print("      VULNERABLE LOGIN SYSTEM")
    print("===================================")

    login()


if __name__ == "__main__":
    main()