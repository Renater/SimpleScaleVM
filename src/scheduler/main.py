#!/usr/bin/python3
"""
Define the Scheduler of the scaling module.

Classes:
    Scheduler
"""

from typing import Dict, Union
from apscheduler.schedulers.background import BackgroundScheduler
from providers.main import Provider
from scheduler.service import SchedulerService
from settings import ENABLE_AUTOSCALING
from autoscaler.main import AutoScalerService


class Scheduler():
    """Scheduler of the scaling module."""

    job_queue: BackgroundScheduler
    service: SchedulerService
    autoscaler: Union[AutoScalerService, None]

    def __init__(
        self,
        provider: Provider,
        port: int,
        replica_configuration: Dict[str, Union[str, int]],
    ):

        self.service = SchedulerService(provider, replica_configuration)
        self.job_queue = BackgroundScheduler()
        self.autoscaler = None

        if ENABLE_AUTOSCALING:
            self.autoscaler = AutoScalerService(provider, port)
            self.job_queue.add_job(self.autoscaler.loop, "interval", minutes=1)
            self.job_queue.add_job(
                lambda : self.service.loop(self.autoscaler.getMaster),
                "interval",
                minutes=1
            )
        else:
            self.job_queue.add_job(self.service.loop, "interval", minutes=1)

    def start(self):
        """Start the scheduling of all jobs in the job queue."""

        self.job_queue.start()

    def stop(self):
        """Start the scheduler."""

        self.job_queue.shutdown()
