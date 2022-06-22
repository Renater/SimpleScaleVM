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
    REPLICA_API_PROTOCOL,
    REPLICA_API_PATH,
    REPLICA_API_CAPACITY_KEY,
    REPLICA_API_TERMINATION_KEY,
)
from providers.main import Provider


if __name__ == "__main__":
    provider = Provider(PROVIDER)
    scheduler = Scheduler(provider, {
        "protocol": REPLICA_API_PROTOCOL,
        "path": REPLICA_API_PATH,
        "capacity_key": REPLICA_API_CAPACITY_KEY,
        "termination_key": REPLICA_API_TERMINATION_KEY,
    })
    server = ServerLauncher(APP_HOST, APP_PORT)

    scheduler.start()
    server.serve()
    provider.service.close()
    scheduler.stop()
