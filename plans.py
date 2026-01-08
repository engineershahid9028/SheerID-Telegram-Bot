
from datetime import datetime, date
from db import get_conn

def check_plan(user_id):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("SELECT expires_at, daily_limit, used_today, last_reset FROM user_plans WHERE user_id=%s",(user_id,))
    row = cur.fetchone(); conn.close()
    if not row: return False, "No active plan"
    expires, limit, used, last_reset = row
    if datetime.utcnow() > expires: return False, "Plan expired"
    if last_reset != date.today():
        reset_daily(user_id); used = 0
    if used >= limit: return False, "Daily limit reached"
    return True, None

def consume(user_id):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("UPDATE user_plans SET used_today = used_today + 1 WHERE user_id=%s",(user_id,))
    conn.commit(); conn.close()

def reset_daily(user_id):
    conn = get_conn(); cur = conn.cursor()
    cur.execute("UPDATE user_plans SET used_today=0, last_reset=CURRENT_DATE WHERE user_id=%s",(user_id,))
    conn.commit(); conn.close()
