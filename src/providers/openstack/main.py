#!/usr/bin/python3
"""
Set the OpenStack provider for the autoscaling module.

Classes:
    ProviderService
"""

from typing import List
from threading import Thread
import openstack
from providers.openstack.settings import (
    OPENSTACK_FLAVOR,
    OPENSTACK_IMAGE,
    OPENSTACK_IP_VERSION,
    OPENSTACK_KEYPAIR,
    OPENSTACK_METADATA_KEY,
    OPENSTACK_METADATA_VALUE,
    OPENSTACK_NETWORK,
    OPENSTACK_CLOUD_INIT_FILE,
)
from providers.schema import BaseProviderService
from providers.replica import Replica, ReplicaStatus


class ProviderService(BaseProviderService):
    """Service of the Openstack provider."""

    def __init__(self):

        self.connector = openstack.connect(cloud="envvars")

    def list(self) -> List[Replica]:

        servers = []

        for server_object in self.connector.compute.servers():
            server = server_object.to_dict()

            if (
                OPENSTACK_METADATA_KEY in server["metadata"] and
                server["metadata"][OPENSTACK_METADATA_KEY] == OPENSTACK_METADATA_VALUE
            ):
                # If a deletion order has been sent, do not count the virtual machine
                if server["task_state"] == "deleting":
                    continue

                server_status = ReplicaStatus.ERROR
                server_address = None

                # Power state of the virtual machine
                # ref: https://docs.openstack.org/nova/latest/reference/vm-states.html
                if server["vm_state"] == "building":
                    server_status = ReplicaStatus.CREATING
                elif server["vm_state"] == "active":
                    server_status = ReplicaStatus.CREATED_UNKNOWN

                # If an active VM does not have any IP address yet, count it as creating
                if (
                    OPENSTACK_NETWORK not in server["addresses"] and
                    server_status == ReplicaStatus.CREATED_UNKNOWN
                ):
                    server_status = ReplicaStatus.CREATING

                # Get the IP address of the virtual machine
                elif OPENSTACK_NETWORK in server["addresses"]:
                    for server_port in server["addresses"][OPENSTACK_NETWORK]:
                        if server_port["version"] == OPENSTACK_IP_VERSION:
                            server_address = server_port["addr"]
                            break

                replica = Replica(server["id"], server_address, server_status)
                servers.append(replica)

        return servers

    def create(self, count: int = 1):

        def creation_function():
            server_configuration = {
                "name": "server",
                "image": OPENSTACK_IMAGE,
                "flavor": OPENSTACK_FLAVOR,
                "network": OPENSTACK_NETWORK,
                "meta": { OPENSTACK_METADATA_KEY: OPENSTACK_METADATA_VALUE },
            }

            # Add optional key pair
            if OPENSTACK_KEYPAIR:
                server_configuration["key_name"] = OPENSTACK_KEYPAIR

            # Add optional cloud-init
            if OPENSTACK_CLOUD_INIT_FILE:
                with open(OPENSTACK_CLOUD_INIT_FILE, encoding="utf-8") as cloud_init_file:
                    server_configuration["userdata"] = cloud_init_file.read()

            return self.connector.create_server(**server_configuration)

        for _ in range(count):
            thread = Thread(target=creation_function)
            thread.start()

    def delete(self, server_id: str):

        self.connector.delete_server(server_id)

    def close(self):

        self.connector.close()
