# SimpleScaleVM

Python module to manage the autoscaling of a cluster of virtual machines.


## Configuration

All the configuration is contained in the `.env` environment file. To initialize it, launch the following command:

```bash
make .env
```

Besides, the following values may be overwritten to configure the module:
* `APP_HOST`: host of the HTTP server.
* `APP_PORT`: port of the HTTP server.
* `PROVIDER`: provider that is used to deploy virtual resources (the only available value is `openstack`).

The environment variables that are specific to the providers are detailed in the following subsections.

### Openstack provider configuration

The following values should be overwritten to configure the connection to the Openstack provider:
* `OS_AUTH_URL`: URL of the Openstack endpoint.
* `OS_USERNAME`: name of the Openstack user.
* `OS_PASSWORD`: password of the Openstack user.
* `OS_REGION_NAME`: name of the Openstack region.
* `OS_PROJECT_DOMAIN_ID`: ID of the Openstack project domain.
* `OS_USER_DOMAIN_NAME`: name of the Openstack project domain.
* `OS_PROJECT_ID`: ID of the Openstack project.
* `OS_PROJECT_NAME`: name of the Openstack project.
* `OS_INTERFACE`: Openstack interface.
* `OS_IDENTITY_API_VERSION`: version of the Openstack API.
* `OPENSTACK_FLAVOR`: name of the flavor to use for the virtual machines.
* `OPENSTACK_IMAGE`: name of the image to use for the virtual machines.
* `OPENSTACK_NETWORK`: name of the network to use for the virtual machines.
* `OPENSTACK_METADATA_KEY`: metadata key to identify the scaled server pool.
* `OPENSTACK_METADATA_VALUE`: metadata value to identify the scaled server pool.
* `OPENSTACK_KEYPAIR`: name of the keypair that is provisioned on the virtual machines.


## Installation

Python [virtualenv](https://virtualenv.pypa.io/en/latest/) is used to run the module. To install it, launch the following command:

```bash
python3 -m pip install virtualenv
```

To setup the virtualenv and install the requirements, launch the following command:

```bash
make install
```


## Launch the module

To start the module, launch the following command:

```bash
make start
```


## Licensing

Apache License Version 2.0.

See [LICENSE](./LICENSE) to see the full text.
