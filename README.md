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
- Session-based authentication state
- SQLite persistence
- Automated unit tests
- Basic input validation
- Clear demonstration workflow

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
unzip MFA_Capstone_Professional.zip
cd MFA_Capstone_Professional
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Open `http://127.0.0.1:5000`.

For an isolated authorized LAN lab, change the host in `app.py` to `0.0.0.0` and access it only from the lab network.

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
- Debug mode is disabled.
- Basic username/password/code validation is included.

## Production limitations
This is an educational MVP. A production implementation should add HTTPS, CSRF protection, rate limiting, login throttling/lockout, audit logging, secure secret management, secure cookie deployment, monitoring, and stronger account-recovery policy.

## Authorized use
Run only against systems you own or are explicitly authorized to test. Use synthetic accounts and data in an isolated lab.
