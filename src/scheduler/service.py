#!/usr/bin/python3
"""
Define the service of the Scheduler.

Classes:
    SchedulerService
"""

import math
from typing import Callable, Dict, Union
from scheduler.api import APIService
from providers.main import Provider
from providers.replica import ReplicaStatus

class SchedulerService:
    """Scheduler service of the scaling module."""

    provider: Provider
    api: APIService
    replica_capacity: int
    min_available_resources: int


    def __init__(self, provider: Provider, replica_configuration: Dict[str, Union[str, int]]):
        self.provider = provider
        self.api = APIService({
            "protocol": replica_configuration["api_protocol"],
            "port": replica_configuration["api_port"],
            "path": replica_configuration["api_path"],
            "capacity_key": replica_configuration["api_capacity_key"],
            "termination_key": replica_configuration["api_termination_key"],
        })
        self.replica_capacity = replica_configuration["capacity"]
        self.min_available_resources = replica_configuration["min_available_resources"]

    def loop(self, is_master: Callable[[None], bool] = lambda : True):
        """Check the status of all replicas, delete the replicas that should be deleted and
        create a number of replicas to always have the minimum number of available resources."""

        if is_master():

            replicas = self.provider.service.list()
            healthy_replicas = []
            replicas_to_delete = []
            available_resources = 0

            for replica in replicas:
                # If the replica is in error state, add it to the deletion list
                if replica.status == ReplicaStatus.ERROR:
                    replicas_to_delete.append((replica, "error"))
                    continue

                # If the replica is creating, add the potential resources to the count
                if replica.status == ReplicaStatus.CREATING:
                    available_resources += self.replica_capacity
                    continue

                # Check the status of the replica
                status = self.api.get_status(replica)
                if status:
                    if status["termination"]:
                        replicas_to_delete.append((replica, "termination"))
                    else:
                        healthy_replicas.append(replica)
                        available_resources += status["capacity"]

            # Find all replicas without external address
            available_replicas = [
                replica for replica in healthy_replicas if not replica.external_address
            ]

            for replica, reason in replicas_to_delete:
                print((
                    f"Scaling down ({reason}): replica with ID "
                    + f"{replica.identifier} has been scheduled for deletion."
                ))

                migration_replica = None
                # If replica has an external address, reassign it
                if replica.external_address and len(available_replicas) > 0:
                    migration_replica = available_replicas.pop()
                    print((
                        f"Address {replica.external_address} reassigned from replica with ID "
                        + f"{replica.identifier} to replica with ID {migration_replica.identifier}."
                    ))

                self.provider.service.delete(replica, migration_replica)

            # Assign the available external addresses
            external_address_assignment = self.provider.service.assign(available_replicas)
            for external_address in external_address_assignment:
                print((
                    f"Address {external_address} has been assigned to replica with ID "
                    + f"{external_address_assignment[external_address].identifier}."
                ))

            # If there are not enough available resources, create replicas
            if available_resources < self.min_available_resources:
                replicas_to_create = math.ceil(
                    (self.min_available_resources - available_resources) / self.replica_capacity
                )

                print(f"Scaling up: {replicas_to_create} replicas"
                    + "has been scheduled for creation.")
                self.provider.service.create(replicas_to_create)
