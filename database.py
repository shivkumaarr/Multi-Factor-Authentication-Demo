import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mfa_demo.db")

def connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        totp_secret TEXT NOT NULL
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS recovery_codes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        code_hash TEXT NOT NULL,
        used INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
    conn.commit()
    conn.close()

def create_user(username, password_hash, totp_secret):
    conn = connection()
    try:
        cur = conn.execute(
            "INSERT INTO users(username,password_hash,totp_secret) VALUES(?,?,?)",
            (username, password_hash, totp_secret)
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user(username):
    conn = connection()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return row

def get_user_by_id(user_id):
    conn = connection()
    row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return row

def save_recovery_codes(user_id, hashes):
    conn = connection()
    conn.execute("DELETE FROM recovery_codes WHERE user_id=?", (user_id,))
    conn.executemany(
        "INSERT INTO recovery_codes(user_id,code_hash,used) VALUES(?,?,0)",
        [(user_id, h) for h in hashes]
    )
    conn.commit()
    conn.close()

def get_unused_recovery_code(user_id, code_hash):
    conn = connection()
    row = conn.execute(
        "SELECT * FROM recovery_codes WHERE user_id=? AND code_hash=? AND used=0",
        (user_id, code_hash)
    ).fetchone()
    conn.close()
    return row

def mark_recovery_code_used(code_id):
    conn = connection()
    conn.execute("UPDATE recovery_codes SET used=1 WHERE id=?", (code_id,))
    conn.commit()
    conn.close()

def recovery_stats(user_id):
    conn = connection()
    row = conn.execute(
        "SELECT COUNT(*) total, COALESCE(SUM(used),0) used FROM recovery_codes WHERE user_id=?",
        (user_id,)
    ).fetchone()
    conn.close()
    return row["total"], row["used"]
