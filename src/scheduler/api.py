#!/usr/bin/python3
"""
Define the API service on replicas.

Classes:
    APIService
"""

from typing import Dict, Union
import requests
from providers.replica import Replica


class APIService:
    """Service responsible to contact the API of replicas."""

    protocol: str
    port: int
    path: str
    capacity_key: str
    termination_key: str

    def __init__(self, api_configuration: Dict[str, Union[str, int]]):
        self.protocol = api_configuration["protocol"]
        self.port = api_configuration["port"]
        self.path = api_configuration["path"]
        self.capacity_key = api_configuration["capacity_key"]
        self.termination_key = api_configuration["termination_key"]

    def get_status(self, replica: Replica) -> Union[Dict[str, Union[int, bool]], None]:
        """Get the status of a replica."""

        uri = f"{self.protocol}://{replica.address}:{self.port}{self.path}"

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
