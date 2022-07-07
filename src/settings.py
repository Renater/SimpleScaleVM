#!/usr/bin/python3
"""
Configure the autoscaling module.

Variables:
    APP_HOST
    APP_PORT
    EXTERNAL_ADDRESS_MANAGEMENT
    PROVIDER
    REPLICA_CAPACITY
    REPLICA_MIN_AVAILABLE_RESOURCES
    REPLICA_API_PROTOCOL
    REPLICA_API_PORT
    REPLICA_API_PATH
    REPLICA_API_CAPACITY_KEY
    REPLICA_API_TERMINATION_KEY
"""

import os
import dotenv


# Load the `.env` file
dotenv.load_dotenv()

# Create environment parameters
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
EXTERNAL_ADDRESS_MANAGEMENT = os.getenv("EXTERNAL_ADDRESS_MANAGEMENT", "false") != "false"
PROVIDER = os.getenv("PROVIDER", "openstack")
REPLICA_CAPACITY = int(os.getenv("REPLICA_CAPACITY", "1"))
REPLICA_MIN_AVAILABLE_RESOURCES = int(os.getenv("REPLICA_MIN_AVAILABLE_RESOURCES", "3"))
REPLICA_API_PROTOCOL = os.getenv("REPLICA_API_PROTOCOL", "http")
REPLICA_API_PORT = int(os.getenv("REPLICA_API_PORT", "8080"))
REPLICA_API_PATH = os.getenv("REPLICA_API_PATH", "/")
REPLICA_API_CAPACITY_KEY = os.getenv("REPLICA_API_CAPACITY_KEY", "capacity")
REPLICA_API_TERMINATION_KEY = os.getenv("REPLICA_API_TERMINATION_KEY", "termination")
