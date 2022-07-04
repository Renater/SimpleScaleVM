# SimpleScaleVM

This repository hosts a Python module to manage the autoscaling of a cluster of virtual machines called **replicas**. These replicas each hold a certain number of **resources** that constitute the autoscaling cost of replicas.


## Configuration

All the configuration is contained in the `.env` environment file. To initialize it, launch the following command:

```bash
make .env
```

Besides, the following values may be overwritten to configure the module:
* `VERSION`: semantic version of the project (only used for releasing the Docker image).
* `APP_HOST`: host of the HTTP server.
* `APP_PORT`: port of the HTTP server.
* `REPLICA_CAPACITY`: total number of resources per replica.
* `REPLICA_MIN_AVAILABLE_RESOURCES`: minimum number of resources that should be available at all times.
* `REPLICA_API_PROTOCOL`: protocol to use to contact the API on replicas.
* `REPLICA_API_PORT`: port to use to contact the API on replicas.
* `REPLICA_API_PATH`: path to use to contact the API on replicas.
* `REPLICA_API_CAPACITY_KEY`: key of the API response that corresponds to the number of available resources on the replica.
* `REPLICA_API_TERMINATION_KEY`: key of the API response that corresponds to the boolean indicating if the replica should be terminated.
* `EXTERNAL_ADDRESS_MANAGEMENT`: boolean that indicates if the scaler should manage external addresses.
* `PROVIDER`: provider that is used to deploy replicas (the only available value is `openstack`).

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
* `OPENSTACK_IP_VERSION`: IP version to use for virtual machines.
* `OPENSTACK_NETWORK`: name of the network to use for the virtual machines.
* `OPENSTACK_METADATA_KEY`: metadata key to identify the scaled server pool.
* `OPENSTACK_METADATA_VALUE`: metadata value to identify the scaled server pool.
* `OPENSTACK_FLOATING_IP_DESCRIPTION`: description of the floating IPs that should be assigned (only used when `EXTERNAL_ADDRESS_MANAGEMENT` is enabled).
* `OPENSTACK_KEYPAIR`: name of the keypair that is provisioned on the virtual machines.
* `OPENSTACK_CLOUD_INIT_FILE`: path to a cloud-init file to launch on virtual machines at creation.


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


## Working with Docker

Once your project is configured, you can start working with Docker by building, launching and releasing on DockerHub with the respective commands:

```bash
make build
make start-docker
make release
```

Note that each provider has its specific Docker image version which contains the provider requirements: the Docker tag format is `<provider>-<version>`.


## Tests

In order to be able to test the autoscaling module, a simple HTTP webserver that listens on all GET requests and returns replica API responses can be launched with the following command:

```bash
make mock
```

Besides, this webserver may be configured in the `tests/mock.env` file with the following environment variables:
* `MOCK_HOST`: host of the HTTP server.
* `MOCK_PORT`: port of the HTTP server.
* `MOCK_CAPACITY_KEY`: key of the API response that corresponds to the number of available resources on the replica.
* `MOCK_TERMINATION_KEY`: key of the API response that corresponds to the boolean indicating if the replica should be terminated.
* `MOCK_CAPACITY_VALUE`: value linked to the `MOCK_CAPACITY_KEY` key.
* `MOCK_TERMINATION_VALUE`: value linked to the `MOCK_TERMINATION_KEY` key.


## Licensing

Apache License Version 2.0.

See [LICENSE](./LICENSE) to see the full text.
