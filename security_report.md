# Secure Code Assessment Report

## CodSoft Cyber Security Internship — Task 3

**Author:** Aditya Kumar Singh

---

## 1. Objective

The objective of this task is to review a vulnerable Python login application, identify security weaknesses, and implement secure coding practices to mitigate the identified vulnerabilities.

The assessment focuses on authentication security, password protection, SQL injection prevention, and information disclosure.

---

## 2. Application Assessed

The application is a simple Python-based login system using SQLite as its database.

Two versions were developed:

- `vulnerable_app.py` — intentionally insecure implementation
- `secure_app.py` — remediated implementation

---

## 3. Security Findings

### Finding 1 — Hardcoded Credential

**Severity:** High

**Location:** `vulnerable_app.py`

The vulnerable application contains a credential directly in the source code:

```python
ADMIN_PASSWORD = "admin123"