#!/usr/bin/python3
"""
Define the service of the Scheduler.

Classes:
    SchedulerService
"""

import math
from typing import Dict, Union
from providers.main import Provider
from providers.replica import ReplicaStatus
from scheduler.api import APIService


class SchedulerService:
    """Scheduler service of the autoscaling module."""

    provider: Provider
    api: APIService
    replica_capacity: int
    min_available_resources: int


    def __init__(self, provider: Provider, replica_configuration: Dict[str, Union[str, int]]):
        self.provider = provider
        self.api = APIService(
            replica_configuration["api_protocol"],
            replica_configuration["api_port"],
            replica_configuration["api_path"],
            replica_configuration["api_capacity_key"],
            replica_configuration["api_termination_key"],
        )
        self.replica_capacity = replica_configuration["capacity"]
        self.min_available_resources = replica_configuration["min_available_resources"]

    def loop(self):
        """Check the status of all replicas, delete the replicas that should be deleted and
        create a number of replicas to always have the minimum number of available resources."""

        replicas = self.provider.service.list()
        available_resources = 0

        for replica in replicas:
            # If the replica is in error state, delete it
            if replica.status == ReplicaStatus.ERROR:
                print((
                    f"Scaling down (error): replica with ID {replica.identifier}"
                    + " has been scheduled for deletion."
                ))
                self.provider.service.delete(replica.identifier)
                continue

            # If the replica is creating, add the potential resources to the count
            if replica.status == ReplicaStatus.CREATING:
                available_resources += self.replica_capacity
                continue

            status = self.api.get_status(replica)
            if status:
                # If the replica should be deleted, do it
                if status["termination"]:
                    print((
                        f"Scaling down: replica with ID {replica.identifier}"
                        + " has been scheduled for deletion."
                    ))
                    self.provider.service.delete(replica.identifier)
                    continue

                # Add the available resources to the global count
                available_resources += status["capacity"]

        # If there are not enough available resources, create replicas
        if available_resources < self.min_available_resources:
            replicas_to_create = math.ceil(
                (self.min_available_resources - available_resources) / self.replica_capacity
            )
            print(f"Scaling up: {replicas_to_create} replicas has been scheduled for creation.")
            self.provider.service.create(replicas_to_create)
