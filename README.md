# Secure File Sharing System

## CodSoft Cyber Security Internship — Task 5

A Python Flask-based secure file-sharing application that provides authenticated access, encrypted file storage, and controlled file downloads.

## Features

- User registration
- Secure password hashing
- User authentication
- Session-based access control
- Role-based access control
- File upload
- File encryption using Fernet
- Encrypted file storage
- Secure file download and decryption
- File size restriction
- Secure filename handling
- Logout functionality

## Technology Stack

- Python
- Flask
- SQLite
- Cryptography
- HTML/CSS

## Security Measures

### Password Protection

User passwords are stored using Werkzeug password hashing instead of plain-text passwords.

### File Encryption

Uploaded files are encrypted using Fernet symmetric encryption before being stored.

### SQL Injection Prevention

Database queries use parameterized SQL statements.

### Secure File Names

Uploaded filenames are processed using `secure_filename()`.

### Session Authentication

Users must be authenticated before accessing the dashboard or downloading files.

### File Size Restriction

Uploads are limited to 10 MB.

### No Persistent Plaintext Download Copy

Files are decrypted in memory during download instead of creating a permanent plaintext copy on the server.

## Project Structure

```text
CODSOFT_TASK05_SECURE_FILE_SHARING/
│
├── app.py
├── crypto_utils.py
├── requirements.txt
├── README.md
├── security_report.md
├── .gitignore
│
├── uploads/
│   └── .gitkeep
│
└── templates/
    ├── login.html
    ├── register.html
    └── dashboard.html