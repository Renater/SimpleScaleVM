#!/usr/bin/python3
"""
Define the replica class.

Classes:
    Replica
    ReplicaStatus
"""

import enum
from typing import Union


class ReplicaStatus(enum.Enum):
    """Status of replicas."""

    CREATING = "CREATING"
    CREATED_UNKNOWN = "CREATED_UNKNOWN"
    ERROR = "ERROR"

class Replica:
    """Replica representation."""

    identifier: str
    status: ReplicaStatus
    address: Union[str, None]
    external_address: Union[str, None]

    def __init__(
        self,
        identifier: str,
        status: ReplicaStatus,
        address: Union[str, None] = None,
        external_address: Union[str, None] = None,
    ):
        self.identifier = identifier
        self.status = status
        self.address = address
        self.external_address = external_address
