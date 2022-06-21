#!/usr/bin/python3
"""
Configure the autoscaling module.

Variables:
    APP_HOST
    APP_PORT
    PROVIDER
    RESOURCE_API_PROTOCOL
    RESOURCE_API_PATH
    RESOURCE_API_CAPACITY_KEY
    RESOURCE_API_TERMINATION_KEY
"""

import os
import dotenv


# Load the `.env` file
dotenv.load_dotenv()

# Create environment parameters
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
PROVIDER = os.getenv("PROVIDER", "openstack")
RESOURCE_API_PROTOCOL = os.getenv("RESOURCE_API_PROTOCOL", "http")
RESOURCE_API_PATH = os.getenv("RESOURCE_API_PATH", "/")
RESOURCE_API_CAPACITY_KEY = os.getenv("RESOURCE_API_CAPACITY_KEY", "capacity")
RESOURCE_API_TERMINATION_KEY = os.getenv("RESOURCE_API_TERMINATION_KEY", "termination")
