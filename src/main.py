#!/usr/bin/python3
"""
Launch the autoscaling module.
"""

from server.launcher import ServerLauncher
from scheduler.main import Scheduler
from settings import (
    APP_HOST,
    APP_PORT,
    PROVIDER,
    RESOURCE_API_PROTOCOL,
    RESOURCE_API_PATH,
    RESOURCE_API_CAPACITY_KEY,
    RESOURCE_API_TERMINATION_KEY,
)
from providers.main import Provider


if __name__ == "__main__":
    provider = Provider(PROVIDER)
    scheduler = Scheduler(provider, {
        "protocol": RESOURCE_API_PROTOCOL,
        "path": RESOURCE_API_PATH,
        "capacity_key": RESOURCE_API_CAPACITY_KEY,
        "termination_key": RESOURCE_API_TERMINATION_KEY,
    })
    server = ServerLauncher(APP_HOST, APP_PORT)

    scheduler.start()
    server.serve()
    provider.service.close()
    scheduler.stop()
