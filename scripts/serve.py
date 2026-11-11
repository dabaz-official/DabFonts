#!/usr/bin/env python3
"""Static server for the demo pages, with caching disabled.

Plain `http.server` sends Last-Modified only, and Chrome happily reuses the
cached font after a rebuild — which makes an updated build look unchanged.
"""
import http.server, os, socketserver, sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8099

# Serve demo/ regardless of where the command was invoked from.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.join(ROOT, "demo"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


with Server(("127.0.0.1", PORT), Handler) as httpd:
    print(f"serving on http://127.0.0.1:{PORT}", flush=True)
    httpd.serve_forever()
