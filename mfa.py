import hashlib
import secrets
import pyotp
import qrcode

def generate_totp_secret():
    return pyotp.random_base32()

def generate_totp_uri(username, secret):
    return pyotp.TOTP(secret).provisioning_uri(
        name=username,
        issuer_name="MFA Capstone Demo"
    )

def verify_totp(secret, code):
    if not code.isdigit() or len(code) != 6:
        return False
    return pyotp.TOTP(secret).verify(code, valid_window=1)

def generate_recovery_codes(count=8):
    return [secrets.token_hex(5).upper() for _ in range(count)]

def hash_recovery_code(code):
    return hashlib.sha256(code.encode("utf-8")).hexdigest()

def make_qr(uri, output_path):
    qrcode.make(uri).save(output_path)
