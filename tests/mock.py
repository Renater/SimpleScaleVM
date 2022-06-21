#!/usr/bin/python3
"""
Mock a virtual resource webserver.

Classes:
    RequestHandler

Variables:
    MOCK_HOST
    MOCK_PORT
    MOCK_CAPACITY_KEY
    MOCK_TERMINATION_KEY
    MOCK_CAPACITY_VALUE
    MOCK_TERMINATION_VALUE
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import dotenv


# Configure the mock environment
dotenv.load_dotenv()
MOCK_HOST = os.getenv("MOCK_HOST", "0.0.0.0")
MOCK_PORT = int(os.getenv("MOCK_PORT", "5555"))
MOCK_CAPACITY_KEY = os.getenv("MOCK_CAPACITY_KEY", "capacity")
MOCK_TERMINATION_KEY = os.getenv("MOCK_TERMINATION_KEY", "termination")
MOCK_CAPACITY_VALUE = int(os.getenv("MOCK_CAPACITY_VALUE", "0"))
MOCK_TERMINATION_VALUE = (os.getenv("MOCK_TERMINATION_VALUE", "false") != "false")

class RequestHandler(BaseHTTPRequestHandler):
    """Request handler of the virtual resource webserver."""

    def do_GET(self):  # pylint: disable=invalid-name
        """Respond to HTTP GET requests."""

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps({
            MOCK_CAPACITY_KEY: MOCK_CAPACITY_VALUE,
            MOCK_TERMINATION_KEY: MOCK_TERMINATION_VALUE,
        }), "utf-8"))

if __name__ == "__main__":
    server = HTTPServer((MOCK_HOST, MOCK_PORT), RequestHandler)
    print(f"Mock server started listening on http://{MOCK_HOST}:{MOCK_PORT}.")
    server.serve_forever()
