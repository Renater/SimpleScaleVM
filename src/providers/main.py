#!/usr/bin/python3
"""
Define the global provider class.

Classes:
    Provider
"""

from providers.imports import import_provider
from providers.schema import BaseProviderService


class Provider:
    """Global replica provider."""

    service: BaseProviderService

    def __init__(self, provider_name: str, external_address_management: bool):
        provider_module = import_provider(provider_name)
        self.service = provider_module.ProviderService(external_address_management)
