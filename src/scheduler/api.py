#!/usr/bin/python3
"""
Define the API service on virtual resources.

Classes:
    APIService
"""

from typing import Dict, Union
import requests
from providers.resource import Resource


class APIService:
    """Service responsible to contact the API of virtual resources."""

    protocol: str
    path: str
    capacity_key: str
    termination_key: str

    def __init__(self, protocol: str, path: str, capacity_key: str, termination_key: str):
        self.protocol = protocol
        self.path = path
        self.capacity_key = capacity_key
        self.termination_key = termination_key

    def get_status(self, resource: Resource) -> Union[Dict[str, Union[int, bool]], None]:
        """Get the status of a virtual resource."""

        uri = f"{self.protocol}://{resource.address}{self.path}"

        try:
            response = requests.get(uri)
        except requests.exceptions.ConnectionError:
            print(f"Error: could not connect to {uri}")
            return None

        response_json = response.json()
        return {
            "capacity": response_json[self.capacity_key],
            "termination": response_json[self.termination_key]
        }
