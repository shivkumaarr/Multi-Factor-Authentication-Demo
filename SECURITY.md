# Security Features and Limitations

## Implemented
1. Password hashing with Werkzeug.
2. TOTP second factor.
3. QR-based TOTP enrollment.
4. Recovery-code hashing.
5. One-time recovery-code enforcement.
6. Session cookie HttpOnly/SameSite settings.
7. Input length/format validation.
8. Debug mode disabled.
9. Recovery-code usage tracking.

## Not included in this educational MVP
- HTTPS certificate configuration
- CSRF protection
- Rate limiting
- Account lockout
- Centralized audit logging
- Production secret storage
- Email/SMS recovery
- Hardware security keys

These omissions are intentional to keep the capstone focused on password + OTP/TOTP authentication with recovery controls.
