#!/usr/bin/python3
"""
Launch the autoscaling module.
"""

from server.launcher import ServerLauncher
from settings import APP_HOST, APP_PORT, PROVIDER
from providers.main import Provider


if __name__ == "__main__":
    provider = Provider(PROVIDER)
    server = ServerLauncher(APP_HOST, APP_PORT)
    server.serve()
