#!/usr/bin/python3
"""
Launch the scaling module.
"""

from server.launcher import ServerLauncher
from scheduler.main import Scheduler
from settings import (
    APP_HOST,
    APP_PORT,
    EXTERNAL_ADDRESS_MANAGEMENT,
    ENABLE_AUTOSCALING,
    AUTOSCALING_HOST_IP_ADDRESS,
    AUTOSCALING_MIN_REPLICA,
    PROVIDER,
    REPLICA_CAPACITY,
    REPLICA_MIN_AVAILABLE_RESOURCES,
    REPLICA_API_PROTOCOL,
    REPLICA_API_PORT,
    REPLICA_API_PATH,
    REPLICA_API_CAPACITY_KEY,
    REPLICA_API_TERMINATION_KEY,
)
from providers.main import Provider


if __name__ == "__main__":
    provider = Provider(PROVIDER, EXTERNAL_ADDRESS_MANAGEMENT)
    scheduler = Scheduler(provider, APP_PORT, {
        "capacity": REPLICA_CAPACITY,
        "min_available_resources": REPLICA_MIN_AVAILABLE_RESOURCES,
        "api_protocol": REPLICA_API_PROTOCOL,
        "api_port": REPLICA_API_PORT,
        "api_path": REPLICA_API_PATH,
        "api_capacity_key": REPLICA_API_CAPACITY_KEY,
        "api_termination_key": REPLICA_API_TERMINATION_KEY,
    },{
        "enabled": ENABLE_AUTOSCALING,
        "min_available_resources": AUTOSCALING_MIN_REPLICA,
        "address": AUTOSCALING_HOST_IP_ADDRESS,
    })

    if ENABLE_AUTOSCALING:
        server = ServerLauncher(APP_HOST, APP_PORT, scheduler.autoscaler.get_master)
    else:
        server = ServerLauncher(APP_HOST, APP_PORT, lambda : True)

    scheduler.start()
    server.serve()
    provider.service.close()
    scheduler.stop()
