#!/usr/bin/python3
"""
Define the HTTP request handler of the scaling module.

Classes:
    ServerRequestHandler
"""

from http.server import BaseHTTPRequestHandler
import json
from typing import Callable
from socketserver import BaseServer


class ServerRequestHandler(BaseHTTPRequestHandler):
    """Request handler of HTTP servers."""

    status_function: Callable[[None], bool]

    def __init__(self, status_function: Callable[[None], bool],
    request: bytes, client_address: tuple[str, int], server: BaseServer) -> None:
        self.status_function = status_function
        super().__init__(request, client_address, server)


    def do_GET(self):  # pylint: disable=invalid-name
        """Respond to HTTP GET requests."""

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(
            json.dumps({"status": 1, "isMaster": self.status_function()}), "utf-8"
        ))


    def do_POST(self):  # pylint: disable=invalid-name
        """Respond to HTTP POST requests."""

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(f"Path: {self.path}", "utf-8"))
