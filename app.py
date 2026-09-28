from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from crypto_utils import encrypt_file, decrypt_file

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "development-only-secret"
)

UPLOAD_FOLDER = "uploads"
DATABASE = "users.db"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def setup_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        connection = get_db()

        try:
            connection.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, hashed_password, "user")
            )

            connection.commit()

        except sqlite3.IntegrityError:
            connection.close()
            return "Username already exists."

        connection.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_db()

        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):

            session["username"] = user["username"]
            session["role"] = user["role"]

            return redirect(url_for("dashboard"))

        return "Invalid username or password."

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    files = os.listdir(UPLOAD_FOLDER)

    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session["role"],
        files=files
    )


@app.route("/upload", methods=["POST"])
def upload():

    if "username" not in session:
        return redirect(url_for("login"))

    file = request.files.get("file")

    if not file or file.filename == "":
        return "No file selected."

    original_path = os.path.join(
        UPLOAD_FOLDER,
        "temp_" + file.filename
    )

    encrypted_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename + ".encrypted"
    )

    file.save(original_path)

    encrypt_file(
        original_path,
        encrypted_path
    )

    os.remove(original_path)

    return redirect(url_for("dashboard"))


@app.route("/download/<filename>")
def download(filename):

    if "username" not in session:
        return redirect(url_for("login"))

    if session["role"] not in ["user", "admin"]:
        return "Access denied."

    encrypted_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    if not os.path.exists(encrypted_path):
        return "File not found."

    decrypted_data = decrypt_file(encrypted_path)

    temp_path = os.path.join(
        UPLOAD_FOLDER,
        "download_" + filename.replace(".encrypted", "")
    )

    with open(temp_path, "wb") as file:
        file.write(decrypted_data)

    return send_file(
        temp_path,
        as_attachment=True,
        download_name=filename.replace(".encrypted", "")
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)