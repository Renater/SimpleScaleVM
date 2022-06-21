#!/usr/bin/python3
"""
Define the Scheduler of the autoscaling module.

Classes:
    Scheduler
"""

from apscheduler.schedulers.background import BackgroundScheduler


def job_example():
    print("job running")

class Scheduler():
    """Scheduler of the autoscaling module."""

    job_queue: BackgroundScheduler

    def __init__(self):
        self.job_queue = BackgroundScheduler()
        self.job_queue.add_job(job_example, "interval", minutes=1)

    def start(self):
        """Start the scheduling of all jobs in the job queue."""

        self.job_queue.start()

    def stop(self):
        """Start the scheduler."""

        self.job_queue.shutdown()
