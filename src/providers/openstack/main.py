#!/usr/bin/python3
"""
Set the OpenStack provider for the autoscaling module.

Classes:
    ProviderService
"""

from typing import Dict
import openstack
from providers.openstack.settings import (
    OPENSTACK_FLAVOR,
    OPENSTACK_IMAGE,
    OPENSTACK_KEYPAIR,
    OPENSTACK_METADATA_KEY,
    OPENSTACK_METADATA_VALUE,
    OPENSTACK_NETWORK,
)
from providers.schema import BaseProviderService


class ProviderService(BaseProviderService):
    """Service of the Openstack provider."""

    def __init__(self):

        self.connector = openstack.connect(cloud="envvars")

    def list(self) -> Dict[str, str]:

        servers = {}

        for server_object in self.connector.compute.servers():
            server = server_object.to_dict()

            if (
                OPENSTACK_METADATA_KEY in server["metadata"] and
                server["metadata"][OPENSTACK_METADATA_KEY] == OPENSTACK_METADATA_VALUE
            ):
                servers[server["id"]] = server["addresses"][OPENSTACK_NETWORK][0]["addr"]

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
