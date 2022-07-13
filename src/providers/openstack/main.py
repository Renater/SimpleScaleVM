#!/usr/bin/python3
"""
Set the OpenStack provider for the scaling module.

Classes:
    ProviderService
"""

from typing import Dict, List, Union
from threading import Thread
import openstack
from providers.openstack.settings import (
    OPENSTACK_FLOATING_IP_DESCRIPTION,
    OPENSTACK_IP_VERSION,
    OPENSTACK_KEYPAIR,
    OPENSTACK_METADATA_KEY,
    OPENSTACK_AUTOSCALER_CLOUD_INIT_FILE,
    OPENSTACK_AUTOSCALER_FLAVOR,
    OPENSTACK_AUTOSCALER_IMAGE,
    OPENSTACK_AUTOSCALER_NAME,
    OPENSTACK_AUTOSCALER_NETWORK,
    OPENSTACK_METADATA_AUTOSCALER_VALUE,
    OPENSTACK_SCALED_CLOUD_INIT_FILE,
    OPENSTACK_SCALED_FLAVOR,
    OPENSTACK_SCALED_IMAGE,
    OPENSTACK_SCALED_NAME,
    OPENSTACK_SCALED_NETWORK,
    OPENSTACK_METADATA_SCALED_VALUE,
)
from providers.schema import BaseProviderService
from providers.replica import Replica, ReplicaStatus


class ProviderService(BaseProviderService):
    """Service of the Openstack provider."""

    def __init__(self, external_address_management: bool):
        super().__init__(external_address_management)
        self.connector = openstack.connect(cloud="envvars")

    def list(self, autoscaling: bool = False) -> List[Replica]:

        def get_external_addresses():
            # Search for external addresses if `EXTERNAL_ADDRESS_MANAGEMENT` is enabled
            external_addresses = {}
            if self.external_address_management:
                for floating_ip_object in self.connector.list_floating_ips():
                    if (
                        floating_ip_object.description == OPENSTACK_FLOATING_IP_DESCRIPTION
                        and floating_ip_object.attached
                    ):
                        external_addresses[
                            floating_ip_object.fixed_ip_address
                        ] = floating_ip_object.floating_ip_address

            return external_addresses


        if autoscaling:
            metadata_value = OPENSTACK_METADATA_AUTOSCALER_VALUE
            network = OPENSTACK_AUTOSCALER_NETWORK
        else:
            metadata_value = OPENSTACK_METADATA_SCALED_VALUE
            network = OPENSTACK_SCALED_NETWORK

        servers = []
        external_addresses = get_external_addresses()

        for server_object in self.connector.compute.servers():
            server = server_object.to_dict()
            if (
                OPENSTACK_METADATA_KEY in server["metadata"] and
                server["metadata"][OPENSTACK_METADATA_KEY] == metadata_value
            ):
                # If a deletion order has been sent, do not count the virtual machine
                if server["task_state"] == "deleting":
                    continue

                server_status = ReplicaStatus.ERROR
                server_address = None
                server_external_address = None

                # Power state of the virtual machine
                # ref: https://docs.openstack.org/nova/latest/reference/vm-states.html
                if server["vm_state"] == "building":
                    server_status = ReplicaStatus.CREATING
                elif server["vm_state"] == "active":
                    server_status = ReplicaStatus.CREATED_UNKNOWN

                # If an active VM does not have any IP address yet, count it as creating
                if (
                    network not in server["addresses"] and
                    server_status == ReplicaStatus.CREATED_UNKNOWN
                ):
                    server_status = ReplicaStatus.CREATING

                # Get the IP address of the virtual machine
                elif network in server["addresses"]:
                    for server_port in server["addresses"][network]:
                        if (
                            server_port["version"] == OPENSTACK_IP_VERSION
                            and server_port["OS-EXT-IPS:type"] == "fixed"
                        ):
                            server_address = server_port["addr"]

                            # Set the external address property
                            server_external_address = external_addresses.get(server_address, None)

                replica = Replica(
                    server["id"],
                    server_status,
                    server_address,
                    server_external_address
                )
                servers.append(replica)

        return servers

    def create(self, count: int = 1, autoscaling: bool = False):

        def creation_function():

            if autoscaling:
                server_configuration = {
                    "name": OPENSTACK_AUTOSCALER_NAME,
                    "image": OPENSTACK_AUTOSCALER_IMAGE,
                    "flavor": OPENSTACK_AUTOSCALER_FLAVOR,
                    "network": OPENSTACK_AUTOSCALER_NETWORK,
                    "meta": { OPENSTACK_METADATA_KEY: OPENSTACK_METADATA_AUTOSCALER_VALUE },
                }
                # Add optional cloud-init
                if OPENSTACK_AUTOSCALER_CLOUD_INIT_FILE:
                    with open(OPENSTACK_AUTOSCALER_CLOUD_INIT_FILE, encoding="utf-8") as file:
                        server_configuration["userdata"] = file.read()
            else:
                server_configuration = {
                    "name": OPENSTACK_SCALED_NAME,
                    "image": OPENSTACK_SCALED_IMAGE,
                    "flavor": OPENSTACK_SCALED_FLAVOR,
                    "network": OPENSTACK_SCALED_NETWORK,
                    "meta": { OPENSTACK_METADATA_KEY: OPENSTACK_METADATA_SCALED_VALUE },
                }
                # Add optional cloud-init
                if OPENSTACK_SCALED_CLOUD_INIT_FILE:
                    with open(OPENSTACK_SCALED_CLOUD_INIT_FILE, encoding="utf-8") as file:
                        server_configuration["userdata"] = file.read()

            # Add optional key pair
            if OPENSTACK_KEYPAIR:
                server_configuration["key_name"] = OPENSTACK_KEYPAIR

            return self.connector.create_server(**server_configuration)

        for _ in range(count):
            thread = Thread(target=creation_function)
            thread.start()

    def delete(self, replica: Replica, migration_replica: Union[Replica, None] = None):

        if replica.external_address:
            floating_ip_object = self.connector.get_floating_ip(replica.external_address)
            self.connector.detach_ip_from_server(replica.identifier, floating_ip_object.id)

            if migration_replica:
                migration_server_object = self.connector.get_server_by_id(
                    migration_replica.identifier,
                )
                self.connector.add_ip_list(migration_server_object, replica.external_address)

        self.connector.delete_server(replica.identifier)

    def assign(self, replicas: List[Replica]) -> Dict[str, Replica]:

        # Return an empty dictionnary in case the `EXTERNAL_ADDRESS_MANAGEMENT` option is disabled
        if not self.external_address_management:
            return {}

        assignments = {}

        available_addresses = []
        for floating_ip_object in self.connector.list_floating_ips():
            if (
                floating_ip_object.description == OPENSTACK_FLOATING_IP_DESCRIPTION
                and not floating_ip_object.attached
            ):
                available_addresses.append(floating_ip_object.floating_ip_address)

        for address in available_addresses:
            if len(replicas) > 0:
                replica = replicas.pop()
                replica_object = self.connector.get_server_by_id(replica.identifier)
                self.connector.add_ip_list(replica_object, address)
                assignments[address] = replica
            else:
                break

        return assignments

    def close(self):

        self.connector.close()
