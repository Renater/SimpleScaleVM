#!/usr/bin/python3
"""
Configure the autoscaling module.

Variables:
    APP_HOST
    APP_PORT
"""

import os
import dotenv


# Load the `.env` file
dotenv.load_dotenv()

# Define global app parameters
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
