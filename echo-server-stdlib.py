#!/usr/bin/env python3
"""
Simple HTTP server that responds with all request details.
No external dependencies - uses only stdlib.
Save as: echo_server.py
Run: python3 echo_server.py
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import sys

class EchoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_PATCH(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def do_HEAD(self):
        self.handle_request()

    def do_OPTIONS(self):
        self.handle_request()

    def handle_request(self):
        # Read body if present
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b''

        # Parse URL and query string
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Prepare response data
        response_data = {
            "method": self.command,
            "path": self.path,
            "raw_path": parsed_url.path,
            "query_string": parsed_url.query,
            "query_params": {k: v if len(v) > 1 else v[0] for k, v in query_params.items()},
            "headers": dict(self.headers),
            "body_raw": raw_body.decode('utf-8', errors='replace') if raw_body else "",
            "body_bytes_length": len(raw_body),
        }

        # Try to pretty-print JSON body if it looks like JSON
        if raw_body:
            try:
                json_body = json.loads(raw_body)
                response_data["body_json"] = json_body
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass  # Not valid JSON, skip

        # Send response
        response_bytes = json.dumps(response_data, indent=2).encode('utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response_bytes))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
        self.wfile.write(response_bytes)

    def log_message(self, format, *args):
        # Optional: quieter logs
        sys.stderr.write(f"{self.address_string()} - - [{self.log_date_time_string()}] {format % args}\n")

def run(server_class=HTTPServer, handler_class=EchoHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Echo server running on http://localhost:{port}")
    print("Send any request - it will respond with full details as JSON")
    httpd.serve_forever()

if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run(port=port)
    