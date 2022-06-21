#!/usr/bin/python3
"""
Define the service of the Scheduler.

Classes:
    SchedulerService
"""

from typing import Dict
from providers.main import Provider
from scheduler.api import APIService


class SchedulerService:
    """Scheduler service of the autoscaling module."""

    provider: Provider
    api: APIService

    def __init__(self, provider: Provider, api_configuration: Dict[str, str]):
        self.provider = provider
        self.api = APIService(
            api_configuration["protocol"],
            api_configuration["path"],
            api_configuration["capacity_key"],
            api_configuration["termination_key"],
        )

    def example(self):
        print(1)
