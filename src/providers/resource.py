#!/usr/bin/python3
"""
Define the virtual resource class.

Classes:
    Resource
"""

import enum


class ResourceStatus(enum.Enum):
    """Status of virtual resources."""

    CREATING = "CREATING"
    CREATED_UNKNOWN = "CREATED_UNKNOWN"
    READY = "READY"
    IN_USE = "IN_USE"
    ERROR = "ERROR"

class Resource:
    """Virtual resource representation."""

    identifier: str
    address: str
    status: ResourceStatus

    def __init__(self, identifier: str, address: str, status: ResourceStatus):
        self.identifier = identifier
        self.address = address
        self.status = status
