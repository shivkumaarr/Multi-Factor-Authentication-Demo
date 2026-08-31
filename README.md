# Multi-Factor Authentication (MFA) Demo — Capstone Project

**Cybersecurity Capstone Project | Cyart Tech Internship**
**Author:** Shiv Kumar

## Project Objective

Implement **password + TOTP-based authentication** with secure recovery controls to demonstrate a basic Multi-Factor Authentication workflow.

## What This Project Demonstrates

* User registration
* Password authentication with Werkzeug password hashing
* TOTP-based second-factor authentication
* QR-code based TOTP enrollment
* TOTP verification
* Recovery-code generation
* Recovery-code hashing before database storage
* One-time recovery-code usage
* Recovery-code reuse prevention
* Basic input validation
* End-to-end authentication workflow

## Architecture

```text
┌─────────────────────┐
│       Browser       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Flask Application  │
└──────────┬──────────┘
           │
           ▼
┌────────────────────────────┐
│   Password Verification    │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│        MFA / TOTP          │
│  • TOTP Secret             │
│  • QR Provisioning         │
│  • TOTP Verification       │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│      Recovery Module       │
│  • Code Generation         │
│  • Code Hashing            │
│  • Reuse Prevention        │
└────────────┬───────────────┘
             │
             ▼
┌─────────────────────┐
│       Database      │
│  • Users            │
│  • Recovery Codes   │
└─────────────────────┘
```

## Setup on Kali Linux

```bash
cd mfa
unzip mfa.zip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Demonstration Workflow

1. Create a test account.
2. Enroll TOTP using the generated QR code.
3. Save the generated recovery codes.
4. Log in using username and password.
5. Verify the TOTP code.
6. Access the authenticated dashboard.
7. Log out.
8. Log in using a recovery code.
9. Attempt to reuse the same recovery code.
10. Verify that the reused code is rejected.

## Security Features

* Passwords are stored as secure password hashes.
* TOTP provides a time-based second authentication factor.
* TOTP enrollment uses QR-code provisioning.
* Recovery codes are hashed before database storage.
* Recovery codes are invalidated after successful use.
* Previously used recovery codes cannot be reused.
* Session cookies use `HttpOnly` and `SameSite=Lax`.
* Username, password, and recovery-code input validation is implemented.

## Environment

Developed and tested in an **isolated and authorized environment** for cybersecurity education and demonstration.

**Technology:** Python | Flask | SQLite | TOTP | Werkzeug | HTML/CSS | Linux
