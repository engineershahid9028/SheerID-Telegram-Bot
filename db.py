
import os, psycopg2
from config import DATABASE_URL

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        credits INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT NOW()
    );
    CREATE TABLE IF NOT EXISTS user_plans (
        user_id BIGINT PRIMARY KEY,
        plan TEXT,
        expires_at TIMESTAMP,
        daily_limit INT,
        used_today INT DEFAULT 0,
        last_reset DATE DEFAULT CURRENT_DATE
    );
    CREATE TABLE IF NOT EXISTS stats (
        id SERIAL PRIMARY KEY,
        user_id BIGINT,
        service TEXT,
        success BOOLEAN,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)
    conn.commit(); cur.close(); conn.close()
