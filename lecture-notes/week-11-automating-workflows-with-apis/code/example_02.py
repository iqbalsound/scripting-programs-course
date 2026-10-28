def already_alerted(conn, entity, hours=24):
    cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours)).isoformat()
    return conn.execute("SELECT 1 FROM alerts WHERE entity=? AND ts>? LIMIT 1", (entity, cutoff)).fetchone() is not None

conn = sqlite3.connect("alerts.db")
conn.execute("CREATE TABLE IF NOT EXISTS alerts (entity TEXT, ts TEXT, action TEXT)")
# ... after a successful send_alert():
conn.execute("INSERT INTO alerts VALUES (?,?,?)", (entity, datetime.datetime.now(datetime.timezone.utc).isoformat(), "webhook"))
conn.commit()
