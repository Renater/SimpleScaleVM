#!/usr/bin/python3
"""
Define the provider service schema.

Functions:
    BaseProviderService
"""

class BaseProviderService:
    """Base of the provider services."""

    def list(self):
        """List all virtual machines in the autoscaling pool."""

    def create(self):
        """Create a virtual machine."""

    def delete(self):
        """Delete a virtual machine."""
