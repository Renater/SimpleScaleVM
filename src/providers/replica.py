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
    address: Union[str, None]
    status: ReplicaStatus

    def __init__(self, identifier: str, address: str, status: ReplicaStatus):
        self.identifier = identifier
        self.address = address
        self.status = status
