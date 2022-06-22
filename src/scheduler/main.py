#!/usr/bin/python3
"""
Define the Scheduler of the autoscaling module.

Classes:
    Scheduler
"""

from typing import Dict, Union
from apscheduler.schedulers.background import BackgroundScheduler
from providers.main import Provider
from scheduler.service import SchedulerService


class Scheduler():
    """Scheduler of the autoscaling module."""

    job_queue: BackgroundScheduler
    service: SchedulerService

    def __init__(self, provider: Provider, replica_configuration: Dict[str, Union[str, int]]):
        self.service = SchedulerService(provider, replica_configuration)
        self.job_queue = BackgroundScheduler()
        self.job_queue.add_job(self.service.loop, "interval", minutes=1)

    def start(self):
        """Start the scheduling of all jobs in the job queue."""

        self.job_queue.start()

    def stop(self):
        """Start the scheduler."""

        self.job_queue.shutdown()
