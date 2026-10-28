from http.server import BaseHTTPRequestHandler, HTTPServer
import json, datetime
calls = 0
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        global calls
        if self.headers.get("Key") != "lab-key":
            return self._send(401, {"errors": [{"detail": "Authentication failed"}]})
        calls += 1
        if calls > 3:
            return self._send(429, {"errors": [{"detail": "Rate limit exceeded"}]})
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self._send(200, {"data": {"ipAddress": "203.0.113.9", "abuseConfidenceScore": 77,
                                  "totalReports": 12, "lastReportedAt": now}})
    def _send(self, code, body):
        b = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
HTTPServer(("127.0.0.1", 8000), H).serve_forever()
