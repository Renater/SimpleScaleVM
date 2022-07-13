#!/usr/bin/python3
"""
Define the autoscaling service of the Scheduler.

Classes:
    AutoScalerService
"""

import math
from providers.main import Provider
from scheduler.api import APIService
from providers.replica import ReplicaStatus
from settings import AUTOSCALING_MIN_REPLICA, AUTOSCALING_HOST_IP_ADDRESS


class AutoScalerService:
    """Scheduler autoscaling service of the scaling module."""

    provider: Provider
    api: APIService
    replica_capacity: int
    min_available_resources: int
    master: bool
    address: str


    def __init__(self, provider: Provider, port: int):
        self.provider = provider
        self.api = APIService({
            "protocol": "http",
            "port": port,
            "path": "/",
            "capacity_key": "status",
            "termination_key": "isMaster"
        })
        self.replica_capacity = 1
        self.min_available_resources = AUTOSCALING_MIN_REPLICA
        self.master = False
        self.address = AUTOSCALING_HOST_IP_ADDRESS

    def get_master(self):
        return self.master

    def loop(self):
        """Check the status of all replicas, delete the replicas that should be deleted and
        create a number of replicas to always have the minimum number of available resources."""

        replicas = self.provider.service.list(autoscaling=True)
        available_resources = 0

        if not self.master:
            is_master_candidate = True

            for replica in replicas:

                if replica.status == ReplicaStatus.CREATED_UNKNOWN and self.address != replica.address:
                    status = self.api.get_status(replica)
                    if status:
                        if replica.address < self.address:
                            is_master_candidate = False
                            break
                        if status["termination"]:
                            is_master_candidate = False
                            break

            if is_master_candidate: # If there is no master in the cluster, the lowest IP address takes this role
                self.master = True
                print("Became master")

        if self.master:

            for replica in replicas:

                # If the replica is in error state, send the deletion order
                if replica.status == ReplicaStatus.ERROR:
                    print((
                        f"Auto-scaling down: replica with ID "
                        + f"{replica.identifier} has been scheduled for deletion."
                    ))
                    self.provider.service.delete(replica)
                    continue

                if self.address != replica.address:

                    # If the replica is creating, add the potential resources to the count
                    if replica.status == ReplicaStatus.CREATING:
                        available_resources += self.replica_capacity
                        continue

                    # Check the status of the replica
                    status = self.api.get_status(replica)
                    if status:
                        available_resources += status["capacity"]
                    else:
                        print((
                        f"Auto-scaling down: replica with ID "
                        + f"{replica.identifier} has been scheduled for deletion."
                        ))
                        self.provider.service.delete(replica)

                else:
                    available_resources += self.replica_capacity

            # If there are not enough available resources, create replicas
            if available_resources < self.min_available_resources:
                replicas_to_create = math.ceil(
                    (self.min_available_resources - available_resources) / self.replica_capacity
                )

                print(f"Auto-scaling up: {replicas_to_create} replicas have been scheduled for creation.")
                self.provider.service.create(replicas_to_create, autoscaling=True)
