# mock_api.py - a tiny local stand-in for the public test API (no internet needed)
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

POSTS = [{"userId": (i % 5) + 1, "id": i, "title": f"case note {i}", "body": f"details for note {i}"}
         for i in range(1, 101)]
TODOS = [{"userId": (i % 5) + 1, "id": i, "title": f"resource task {i}", "completed": i % 3 == 0}
         for i in range(1, 101)]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = {"/posts": POSTS, "/todos": TODOS}.get(self.path)
        code = 200 if data is not None else 404
        body = json.dumps(data if data is not None else {"error": "not found"}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):      # keep the terminal quiet
        pass

if __name__ == "__main__":
    print("Mock API listening on http://127.0.0.1:8765 (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
