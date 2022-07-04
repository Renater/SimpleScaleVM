#!/usr/bin/python3
"""
Define the provider service schema.

Functions:
    BaseProviderService
"""

from typing import Dict, List, Union
from providers.replica import Replica


class BaseProviderService:
    """Base of the provider services."""

    external_address_management: bool

    def __init__(self, external_address_management: bool):
        self.external_address_management = external_address_management

    def list(self) -> List[Replica]:
        """List all virtual machines in the autoscaling pool."""

        return []

    def create(self, count: int):
        """Create a virtual machine."""

    def delete(self, replica: Replica, migration_replica: Union[Replica, None] = None):
        """Delete a virtual machine."""

    def assign(self, replicas: List[Replica]) -> Dict[str, Replica]:
        """Assign available external addresses to replicas."""

    def close(self):
        """Close all connections linked to the provider."""
