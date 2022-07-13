#!/usr/bin/python3
"""
Define the HTTP server launcher of the scaling module.

Classes:
    ServerLauncher
"""

from functools import partial
from http.server import HTTPServer
from typing import Callable
from server.request_handler import ServerRequestHandler


class ServerLauncher():
    """Launcher of HTTP servers."""

    host: str
    port: int
    server: HTTPServer

    def __init__(self, host: str, port: int, status_function: Callable[[None], bool]):
        self.host = host
        self.port = port
        server_request_handler = partial(ServerRequestHandler, status_function)
        self.server = HTTPServer((self.host, self.port), server_request_handler)

    def serve(self):
        """Start the HTTP server and serve it forever."""

        print(f"Server started listening on http://{self.host}:{self.port}.")

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass

        self.stop()
        print("Server stopped.")

    def stop(self):
        """Stop the HTTP server."""

        self.server.server_close()
