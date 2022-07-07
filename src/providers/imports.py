#!/usr/bin/python3
"""
Import the module that corresponds to the specified provider.

Functions:
    import_provider
"""

import importlib.util
import sys
from types import ModuleType


def import_provider(provider_name: str) -> ModuleType:
    """Import the specified provider."""

    try:
        spec = importlib.util.spec_from_file_location(
            "provider",
            f"src/providers/{provider_name}/main.py"
        )
        provider_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(provider_module)
    except ModuleNotFoundError as error:
        print(f"Provider '{provider_name}' could not be imported: {error}")
        sys.exit()

    return provider_module
