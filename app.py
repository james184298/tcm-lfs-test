"""Throwaway LFS test app: serves the first 200 bytes of data.bin.

If Render's build pulled the real LFS content, / shows LFS-REAL-CONTENT-MARKER.
If it only checked out the pointer file, / shows the LFS pointer text instead.
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            here = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(here, "data.bin"), "rb") as f:
                body = f.read(200)
        except Exception as e:  # noqa: BLE001 - test app, show the error
            body = ("ERROR: %s" % e).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
