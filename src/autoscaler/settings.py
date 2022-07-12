#!/usr/bin/python3
"""
Configure the Autoscaling part of the scaling module.

Variables:
    ENABLE_AUTOSCALING
"""

import os


# Create Openstack environment parameters

AUTOSCALING_MIN_REPLICA = int(os.getenv("AUTOSCALING_MIN_REPLICA", "2"))
