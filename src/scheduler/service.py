#!/usr/bin/python3
"""
Define the service of the Scheduler.

Classes:
    SchedulerService
"""

import math
from typing import Dict
from providers.main import Provider
from providers.resource import ResourceStatus
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

    def loop(self):
        """Check the status of all resources, delete the resources that should be deleted
        and create a number of resources to always have a minimum number of replicas."""

        resources = self.provider.service.list()
        available_resources = 0

        for resource in resources:
            # If the resource is in error state, delete it
            if resource.status == ResourceStatus.ERROR:
                self.provider.service.delete(resource.identifier)
                continue

            # If the resource is creating, add the potential resources to the count
            if resource.status == ResourceStatus.CREATING:
                available_resources += 1
                continue

            status = self.api.get_status(resource)
            if status:
                # If the resource should be deleted, do it
                if status["termination"]:
                    self.provider.service.delete(resource.identifier)
                    continue
                available_resources += status["capacity"]

        # If there are not enough available resources, create them
        if available_resources < 5:
            self.provider.service.create(math.ceil((5 - available_resources) / 1))
