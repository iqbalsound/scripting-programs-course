import sqlite3, datetime
conn = sqlite3.connect("alerts.db")
conn.execute("CREATE TABLE IF NOT EXISTS alerts (entity TEXT, ts TEXT, action TEXT)")
def already_alerted(entity, hours=24):
    cutoff = (datetime.datetime.now(datetime.timezone.utc) -datetime.timedelta(hours=hours)).isoformat()
    return conn.execute("SELECT 1 FROM alerts WHERE entity=? AND ts>? LIMIT 1", (entity, cutoff)).fetchone() is not None
# after a successful send: conn.execute("INSERT INTO alerts VALUES (?,?,?)", (entity, now_iso, "email")); conn.commit()
