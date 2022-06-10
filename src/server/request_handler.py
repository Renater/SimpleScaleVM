#!/usr/bin/python3
"""
Define the HTTP request handler of the autoscaling module.

Classes:
    ServerRequestHandler
"""

from http.server import BaseHTTPRequestHandler


class ServerRequestHandler(BaseHTTPRequestHandler):
    """Request handler of autoscaling HTTP servers."""

    def do_GET(self):  # pylint: disable=invalid-name
        """Respond to HTTP GET requests."""

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("API of the autoscaling module", "utf-8"))

    def do_POST(self):  # pylint: disable=invalid-name
        """Respond to HTTP POST requests."""

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(f"Path: {self.path}", "utf-8"))
