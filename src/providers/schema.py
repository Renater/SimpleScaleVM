#!/usr/bin/python3
"""
Define the provider service schema.

Functions:
    BaseProviderService
"""

from typing import List
from providers.resource import Resource


class BaseProviderService:
    """Base of the provider services."""

    def list(self) -> List[Resource]:
        """List all virtual machines in the autoscaling pool."""

        return []

    def create(self, count: int):
        """Create a virtual machine."""

    def delete(self, server_id: str):
        """Delete a virtual machine."""

    def close(self):
        """Close all connections linked to the provider."""
