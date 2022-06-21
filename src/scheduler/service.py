#!/usr/bin/python3
"""
Define the service of the Scheduler.

Classes:
    SchedulerService
"""

from providers.main import Provider


class SchedulerService:
    """Scheduler service of the autoscaling module."""

    provider: Provider

    def __init__(self, provider: Provider):
        self.provider = provider

    def example(self):
        print(1)
