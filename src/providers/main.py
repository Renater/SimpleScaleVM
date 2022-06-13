#!/usr/bin/python3
"""
Define the global provider class.

Classes:
    Provider
"""

from .imports import import_provider

class Provider:
    """Global virtual resource provider."""

    def __init__(self, provider_name: str):
        provider_module = import_provider(provider_name)
        self.service = provider_module.ProviderService()
