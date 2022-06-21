#!/usr/bin/python3
"""
Set the OpenStack provider for the autoscaling module.

Classes:
    ProviderService
"""

from typing import List
import openstack
from providers.openstack.settings import (
    OPENSTACK_FLAVOR,
    OPENSTACK_IMAGE,
    OPENSTACK_IP_VERSION,
    OPENSTACK_KEYPAIR,
    OPENSTACK_METADATA_KEY,
    OPENSTACK_METADATA_VALUE,
    OPENSTACK_NETWORK,
)
from providers.schema import BaseProviderService
from providers.resource import Resource


class ProviderService(BaseProviderService):
    """Service of the Openstack provider."""

    def __init__(self):

        self.connector = openstack.connect(cloud="envvars")

    def list(self) -> List[Resource]:

        servers = []

        for server_object in self.connector.compute.servers():
            server = server_object.to_dict()

            if (
                OPENSTACK_METADATA_KEY in server["metadata"] and
                server["metadata"][OPENSTACK_METADATA_KEY] == OPENSTACK_METADATA_VALUE
            ):
                for server_port in server["addresses"][OPENSTACK_NETWORK]:
                    if server_port["version"] == OPENSTACK_IP_VERSION:
                        resource = Resource(server["id"], server_port["addr"])
                        servers.append(resource)
                        break

        return servers

    def create(self, count: int = 1):

        self.connector.create_server(
            name="gateway",
            image=OPENSTACK_IMAGE,
            flavor=OPENSTACK_FLAVOR,
            key_name=OPENSTACK_KEYPAIR,
            network=OPENSTACK_NETWORK,
            meta={ OPENSTACK_METADATA_KEY: OPENSTACK_METADATA_VALUE },
            min_count=count,
            max_count=count,
        )

    def delete(self, server_id: str):

        self.connector.delete_server(server_id)

    def close(self):

        self.connector.close()
