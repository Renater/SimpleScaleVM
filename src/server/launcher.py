#!/usr/bin/python3
"""
Define the HTTP server launcher of the autoscaling module.

Classes:
    ServerLauncher
"""

from http.server import HTTPServer
from server.request_handler import ServerRequestHandler


class ServerLauncher():
    """Launcher of autoscaling HTTP servers."""

    host = None
    port = None

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server = HTTPServer((self.host, self.port), ServerRequestHandler)

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
