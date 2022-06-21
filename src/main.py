#!/usr/bin/python3
"""
Launch the autoscaling module.
"""

from server.launcher import ServerLauncher
from scheduler.main import Scheduler
from settings import APP_HOST, APP_PORT, PROVIDER
from providers.main import Provider


if __name__ == "__main__":
    provider = Provider(PROVIDER)
    scheduler = Scheduler(provider)
    server = ServerLauncher(APP_HOST, APP_PORT)

    scheduler.start()
    server.serve()
    provider.service.close()
    scheduler.stop()
