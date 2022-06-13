#!/usr/bin/python3
"""
Set the OpenStack provider for the autoscaling module.

Classes:
    ProviderService
"""

import openstack
from providers.openstack.settings import OPENSTACK_NETWORK, OPENSTACK_TAG
from providers.schema import BaseProviderService


class ProviderService(BaseProviderService):
    """Service of the Openstack provider."""

    def __init__(self):

        self.connector = openstack.connect(cloud="envvars")

    def list(self):

        servers = []

        for server_object in self.connector.compute.servers():
            server = server_object.to_dict()

            if OPENSTACK_TAG in server["metadata"]:
                servers.append(server["addresses"][OPENSTACK_NETWORK][0]["addr"])

        return servers

    def create(self):

        print("TO DO")

    def delete(self):

        print("TO DO")

    def close(self):

        self.connector.close()
