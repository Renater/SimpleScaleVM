#!/usr/bin/python3
"""
Configure the Openstack provider.

Variables:
    OPENSTACK_NETWORK
    OPENSTACK_TAG
"""

import os

# Create Openstack environment parameters
OPENSTACK_NETWORK = os.getenv("OPENSTACK_NETWORK", "Ext-Net")
OPENSTACK_TAG = os.getenv("OPENSTACK_TAG", "gateway")
