#!/usr/bin/python3
"""
Launch the autoscaling module.
"""

from server.launcher import ServerLauncher
from settings import APP_HOST, APP_PORT


if __name__ == "__main__":
    server = ServerLauncher(APP_HOST, APP_PORT)
    server.serve()
