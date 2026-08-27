import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, create_user, get_user, get_user_by_id, save_recovery_codes, get_unused_recovery_code, mark_recovery_code_used, recovery_stats
from mfa import generate_totp_secret, generate_totp_uri, verify_totp, generate_recovery_codes, hash_recovery_code, make_qr

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.secret_key = os.environ.get("MFA_DEMO_SECRET", "CHANGE-ME-IN-AN-AUTHORIZED-LAB")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,  # True when deployed behind HTTPS
)

QR_DIR = os.path.join(BASE_DIR, "static", "qr")
os.makedirs(QR_DIR, exist_ok=True)
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if len(username) < 3:
            flash("Username must contain at least 3 characters.")
            return redirect(url_for("register"))
        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return redirect(url_for("register"))

        secret = generate_totp_secret()
        user_id = create_user(username, generate_password_hash(password), secret)
        if not user_id:
            flash("Username already exists.")
            return redirect(url_for("register"))

        codes = generate_recovery_codes()
        save_recovery_codes(user_id, [hash_recovery_code(c) for c in codes])

        uri = generate_totp_uri(username, secret)
        make_qr(uri, os.path.join(QR_DIR, f"{user_id}.png"))

        session["setup_user"] = user_id
        session["setup_username"] = username
        session["setup_secret"] = secret
        session["setup_codes"] = codes
        return redirect(url_for("setup"))

    return render_template("register.html")

@app.route("/setup")
def setup():
    if "setup_user" not in session:
        return redirect(url_for("register"))
    return render_template(
        "setup.html",
        username=session["setup_username"],
        secret=session["setup_secret"],
        codes=session["setup_codes"],
        qr=f"/static/qr/{session['setup_user']}.png"
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_user(username)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.")
            return redirect(url_for("login"))
        session["pending_user"] = user["id"]
        session["pending_username"] = user["username"]
        return redirect(url_for("verify"))
    return render_template("login.html")

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if "pending_user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        user = get_user_by_id(session["pending_user"])
        if user and verify_totp(user["totp_secret"], code):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["auth_method"] = "password + TOTP"
            return redirect(url_for("dashboard"))
        flash("Invalid or expired TOTP code.")
    return render_template("verify.html", username=session.get("pending_username"))

@app.route("/recovery", methods=["GET", "POST"])
def recovery():
    if "pending_user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        code = request.form.get("code", "").strip().upper()
        user_id = session["pending_user"]
        row = get_unused_recovery_code(user_id, hash_recovery_code(code))
        if row:
            mark_recovery_code_used(row["id"])
            user = get_user_by_id(user_id)
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["auth_method"] = "password + recovery code"
            return redirect(url_for("dashboard"))
        flash("Invalid or already-used recovery code.")
    return render_template("recovery.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    total, used = recovery_stats(session["user_id"])
    return render_template(
        "dashboard.html",
        username=session["username"],
        method=session.get("auth_method"),
        total=total,
        used=used
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "ok", "project": "MFA Capstone Demo", "environment": "isolated lab"}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
