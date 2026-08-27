# Short Project Demonstration

## 3–5 minute demo

### 1. Start
```bash
source venv/bin/activate
python3 app.py
```

Open the local application.

### 2. Registration
Create a synthetic test account.

Show:
- Username
- Password field
- MFA QR code
- Recovery codes

### 3. TOTP setup
Scan the QR code with an authenticator application.

Explain:
> The password is the first factor. The TOTP is the second factor and changes periodically.

### 4. Normal MFA login
Enter username and password, then the current TOTP.

Show the authenticated dashboard.

### 5. Recovery control
Log out, authenticate with username/password, choose recovery, and enter one unused recovery code.

### 6. Reuse prevention
Log out and attempt to use the same recovery code again.

Expected result:
`Invalid or already-used recovery code.`

### 7. Explain source code
Show:
- `app.py` — application and authentication workflow
- `mfa.py` — TOTP and recovery-code logic
- `database.py` — database operations
- `tests/test_mfa.py` — automated MFA tests
