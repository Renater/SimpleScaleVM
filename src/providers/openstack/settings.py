#!/usr/bin/python3
"""
Configure the Openstack provider.

Variables:
    OPENSTACK_FLAVOR
    OPENSTACK_IMAGE
    OPENSTACK_KEYPAIR
    OPENSTACK_METADATA_KEY
    OPENSTACK_METADATA_VALUE
    OPENSTACK_NETWORK
"""

import os

# Create Openstack environment parameters
OPENSTACK_FLAVOR = os.getenv("OPENSTACK_FLAVOR", "d2-8")
OPENSTACK_IMAGE = os.getenv("OPENSTACK_IMAGE", "Debian 11")
OPENSTACK_KEYPAIR = os.getenv("OPENSTACK_KEYPAIR")
OPENSTACK_METADATA_KEY = os.getenv("OPENSTACK_METADATA_KEY", "sipmediagw.type")
OPENSTACK_METADATA_VALUE = os.getenv("OPENSTACK_METADATA_VALUE", "gateway")
OPENSTACK_NETWORK = os.getenv("OPENSTACK_NETWORK", "Ext-Net")
