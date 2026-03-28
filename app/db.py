import sqlite3

DB_NAME = "clients.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        income INTEGER,
        job TEXT,
        job_exp INTEGER,
        loans INTEGER,
        status TEXT,
        risk_score REAL,
        decision TEXT,
        ai_comment TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_client(data, risk_score, decision, ai_comment):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO clients (
        age, income, job, job_exp, loans, status,
        risk_score, decision, ai_comment
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(data["age"]),
        int(data["income"]),
        data["job"],
        int(data["job_exp"]),
        int(data["loans"]),
        data["status"],
        risk_score,
        decision,
        ai_comment
    ))

    conn.commit()
    conn.close()