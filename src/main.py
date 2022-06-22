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
    REPLICA_CAPACITY,
    REPLICA_MIN_AVAILABLE_RESOURCES,
    REPLICA_API_PROTOCOL,
    REPLICA_API_PATH,
    REPLICA_API_CAPACITY_KEY,
    REPLICA_API_TERMINATION_KEY,
)
from providers.main import Provider


if __name__ == "__main__":
    provider = Provider(PROVIDER)
    scheduler = Scheduler(provider, {
        "capacity": REPLICA_CAPACITY,
        "min_available_resources": REPLICA_MIN_AVAILABLE_RESOURCES,
        "api_protocol": REPLICA_API_PROTOCOL,
        "api_path": REPLICA_API_PATH,
        "api_capacity_key": REPLICA_API_CAPACITY_KEY,
        "api_termination_key": REPLICA_API_TERMINATION_KEY,
    })
    server = ServerLauncher(APP_HOST, APP_PORT)

    scheduler.start()
    server.serve()
    provider.service.close()
    scheduler.stop()
