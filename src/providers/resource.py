#!/usr/bin/python3
"""
Define the virtual resource class.

Classes:
    Resource
"""


class Resource:
    """Virtual resource representation."""

    identifier: str
    address: str

    def __init__(self, identifier: str, address: str):
        self.identifier = identifier
        self.address = address
