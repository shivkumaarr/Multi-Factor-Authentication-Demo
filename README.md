# Multi-Factor Authentication Demo — Capstone Project

## Project Objective
Implement password + OTP/TOTP authentication with recovery controls in an authorized, isolated lab using synthetic data.

## What this version demonstrates
- User registration
- Password authentication with Werkzeug password hashing
- TOTP-based second authentication factor
- QR-code enrollment
- Recovery-code generation
- Recovery-code hashing before database storage
- One-time recovery-code use
- Basic input validation
- demonstration workflow

## Architecture

```text
Browser
   |
   v
Flask Application
   |
   +--> Password Verification
   |
   +--> MFA Module (mfa.py)
   |       +--> TOTP secret
   |       +--> QR provisioning URI
   |       +--> TOTP verification
   |       +--> Recovery-code generation/hashing
   |
   +--> Database Module (database.py)
           +--> Users
           +--> Recovery Codes
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

Open `http://127.0.0.1:5000`.


## Demonstration
1. Create a synthetic account.
2. Scan the QR code with an authenticator app.
3. Save the recovery codes.
4. Log in with username + password.
5. Enter the TOTP code.
6. Confirm the authenticated dashboard.
7. Log out.
8. Log in again and use one recovery code.
9. Log out and try the same recovery code again.
10. Show that the reused recovery code is rejected.

## Security Features
- Passwords are stored as password hashes.
- TOTP secrets are used for time-based second-factor verification.
- Recovery codes are not stored in plaintext.
- Recovery codes are marked used after successful recovery.
- Used recovery codes cannot be reused.
- Session cookies are HttpOnly and SameSite=Lax.
- username/password/code validation is included.

