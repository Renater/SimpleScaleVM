#!/usr/bin/python3
"""
Configure the Openstack provider.

Variables:
    OPENSTACK_METADATA_KEY
    OPENSTACK_METADATA_VALUE
    OPENSTACK_NETWORK
"""

import os

# Create Openstack environment parameters
OPENSTACK_METADATA_KEY = os.getenv("OPENSTACK_METADATA_KEY", "sipmediagw/type")
OPENSTACK_METADATA_VALUE = os.getenv("OPENSTACK_METADATA_VALUE", "gateway")
OPENSTACK_NETWORK = os.getenv("OPENSTACK_NETWORK", "Ext-Net")
