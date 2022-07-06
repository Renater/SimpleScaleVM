#!/usr/bin/python3
"""
Configure the Autoscaling part of the scaling module.

Variables:
    ENABLE_AUTOSCALING
"""

import os


# Create Openstack environment parameters

ENABLE_AUTOSCALING = os.getenv("ENABLE_AUTOSCALING", "false") == "true"
