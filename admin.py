
from flask import Flask, request
from config import ADMIN_KEY
from db import get_conn

app = Flask(__name__)

@app.before_request
def auth():
    if request.path.startswith("/admin"):
        if request.headers.get("X-Admin-Key") != ADMIN_KEY:
            return {"error":"unauthorized"}, 401

@app.route("/admin/stats")
def stats():
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users"); users = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM user_plans WHERE expires_at > NOW()"); active = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM stats WHERE created_at::date=CURRENT_DATE"); today = cur.fetchone()[0]
    conn.close()
    return {"users":users,"active_plans":active,"verifications_today":today}

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    # Telegram webhook endpoint is wired in main.py
    return "ok"
