#!/usr/bin/python3
"""
Configure the autoscaling module.

Variables:
    APP_HOST
    APP_PORT
    PROVIDER
"""

import os
import dotenv


# Load the `.env` file
dotenv.load_dotenv()

# Create environment parameters
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
PROVIDER = os.getenv("PROVIDER", "openstack")
