#!/usr/bin/python3
"""
Define the service of the Scheduler.

Classes:
    SchedulerService
"""

import math
from typing import Dict
from providers.main import Provider
from providers.replica import ReplicaStatus
from scheduler.api import APIService


class SchedulerService:
    """Scheduler service of the autoscaling module."""

    provider: Provider
    api: APIService

    def __init__(self, provider: Provider, api_configuration: Dict[str, str]):
        self.provider = provider
        self.api = APIService(
            api_configuration["protocol"],
            api_configuration["path"],
            api_configuration["capacity_key"],
            api_configuration["termination_key"],
        )

    def loop(self):
        """Check the status of all replicas, delete the replicas that should be deleted and
        create a number of replicas to always have the minimum number of available resources."""

        replicas = self.provider.service.list()
        available_resources = 0

        for replica in replicas:
            # If the replica is in error state, delete it
            if replica.status == ReplicaStatus.ERROR:
                self.provider.service.delete(replica.identifier)
                continue

            # If the replica is creating, add the potential resources to the count
            if replica.status == ReplicaStatus.CREATING:
                available_resources += 1
                continue

            status = self.api.get_status(replica)
            if status:
                # If the replica should be deleted, do it
                if status["termination"]:
                    self.provider.service.delete(replica.identifier)
                    continue

                # Add the available resources to the global count
                available_resources += status["capacity"]

        # If there are not enough available resources, create replicas
        if available_resources < 5:
            self.provider.service.create(math.ceil((5 - available_resources) / 1))
