# Quick reference

-   **Maintained by**:
    [Renater](https://github.com/Renater) (contact@renater.fr)

-   **Where to get help**:
    [the SimpleScaleVM official repository](https://github.com/Renater/SimpleScaleVM)

-   **Where to file issues**:
    [https://github.com/Renater/SimpleScaleVM/issues](https://github.com/Renater/SimpleScaleVM/issues)

-   **Supported architecture**:
    `amd64`

-   **Source of this description**:
    [documentation on the SimpleScaleVM repository](https://github.com/Renater/SimpleScaleVM/tree/main/docs/dockerhub.md)

# Supported tags

-   `openstack-2.0.0`, `openstack-2.0`, `openstack-2`, `openstack-latest`

-   `openstack-1.1.2`, `openstack-1.1`, `openstack-1`

-   `openstack-1.1.1`

-   `openstack-1.1.0`

-   `openstack-1.0.0`, `openstack-1.0`

-   `openstack-0.1.0`, `openstack-0.1`, `openstack-0` (pre-release)


# What is SimpleScaleVM?

SimpleScaleVM is a module written in Python that manages the scaling of a cluster of virtual resources based on HTTP metrics. Its many features include:

-   **Scheduled resource management**:
    The Scaler includes a scheduler that fetches the state of the infrastructure every minute and create or delete replicas according to their status and the Scaler configuration.

-   **Multi-provider support**:
    The Scaler has been designed to be easily adapted on several cloud providers (the only available provider in this repository is [OpenStack](https://wiki.openstack.org/wiki/Main_Page)).

-   **HTTP server for monitoring**:
    A simple HTTP webserver is included in this module to be able to check its status at any time.

-   **External address management**:
    The module includes a _Keepalived-like_ optional feature that makes sure a pool of external addresses are assigned to healthy replicas.


# How to use this image?

## Start a `simplescalevm` server instance

Starting a SimpleScaleVM instance is simple; for instance, to start an instance with the OpenStack provider:

```bash
docker run -p 8000:8000 \
           -e PROVIDER=openstack \
           -e OS_AUTH_URL=<OpenStack endpoint> \
           -e OS_USERNAME=<OpenStack username> \
           -e OS_PASSWORD=<OpenStack password> \
           -e OS_REGION_NAME=<OpenStack region> \
           -e OS_PROJECT_ID=<OpenStack project ID> \
           -e OS_PROJECT_NAME=<OpenStack project name> \
           -e OPENSTACK_FLAVOR=<OpenStack flavor name> \
           -e OPENSTACK_IMAGE=<OpenStack image name> \
           -e OPENSTACK_NETWORK=<OpenStack network name> \
           renater/simplescalevm:openstack-latest
```

## ... via [`docker stack deploy`](https://docs.docker.com/engine/reference/commandline/stack_deploy/) or [`docker-compose`](https://github.com/docker/compose)

Example `stack.yml` for `simplescalevm` with the OpenStack provider:

```yaml
version: "3"

services:
  simplescalevm:
    image: renater/simplescalevm:openstack-latest
    container_name: simplescalevm
    hostname: simplescalevm
    restart: always
    ports:
      - 8000:8000
    volumes:
      - ./cloud-init.sh:/cloud-init.sh
    environment:
      - PROVIDER=openstack
      - OS_AUTH_URL=<OpenStack endpoint>
      - OS_USERNAME=<OpenStack username>
      - OS_PASSWORD=<OpenStack password>
      - OS_REGION_NAME=<OpenStack region>
      - OS_PROJECT_ID=<OpenStack project ID>
      - OS_PROJECT_NAME=<OpenStack project name>
      - OPENSTACK_FLAVOR=<OpenStack flavor name>
      - OPENSTACK_IMAGE=<OpenStack image name>
      - OPENSTACK_NETWORK=<OpenStack network name>
```

Run `docker stack deploy -c stack.yml simplescalevm` (or `docker-compose -f stack.yml up`), wait for it to initialize completely, and visit `http://localhost:8000`.

## Container shell access and viewing SimpleScaleVM logs

The `docker exec` command allows you to run commands inside a Docker container. The following command line will give you a bash shell inside your `simplescalevm` container:

```bash
docker exec -it simplescalevm /bin/sh
```

The log is available through Docker's container log:

```bash
docker logs simplescalevm
```

## Scaler environment variables

When you start the `simplescalevm` image, you can adjust the Scaler configuration of the SimpleScaleVM instance by passing one or more optional environment variables on the `docker run` command line or in the Docker-compose file.

### APP_HOST ###

Host of the HTTP server. Default value is `0.0.0.0`.

### APP_PORT ###

Port of the HTTP server. Default value is `8000`.

### REPLICA_CAPACITY ###

Total number of resources per replica. Default value is `1`.

### REPLICA_MIN_AVAILABLE_RESOURCES ###

Minimum number of resources that should be available at all times. Default value is `3`.

### REPLICA_API_PROTOCOL ###

Protocol to use to contact the API on replicas. Default value is `http`.

### REPLICA_API_PORT ###

Port to use to contact the API on replicas. Default value is `8080`.

### REPLICA_API_PATH ###

Path to use to contact the API on replicas. Default value is `/`.

### REPLICA_API_CAPACITY_KEY ###

Key of the API response that corresponds to the number of available resources on the replica. Default value is `capacity`.

### REPLICA_API_TERMINATION_KEY ###

Key of the API response that corresponds to the boolean indicating if the replica should be terminated. Default value is `termination`.

### EXTERNAL_ADDRESS_MANAGEMENT ###

Boolean that indicates if the scaler should manage external addresses. Default value is `false`.

### PROVIDER ###

Provider that is used to deploy replicas (the only available value is openstack). Default value is `openstack`.

## Provider environment variables

In addition to the environment variables used to configure the Scaler, you have to define the provider configuration by passing environment variables on the `docker run` command line or in the Docker-compose file. The following variables permits to configure the OpenStack provider.

### OS_AUTH_URL ###

URL of the Openstack endpoint. Default value is `https://auth.cloud.ovh.net/v3`.

### OS_USERNAME ###

Name of the Openstack user. **Required**.

### OS_PASSWORD ###

Password of the Openstack user. **Required**.

### OS_REGION_NAME ###

Name of the Openstack region. Default value is `SBG7`.

### OS_PROJECT_DOMAIN_ID ###

ID of the Openstack project domain. Default value is `default`.

### OS_USER_DOMAIN_NAME ###

Name of the Openstack project domain. Default value is `Default`.

### OS_PROJECT_ID ###

ID of the Openstack project. **Required**.

### OS_PROJECT_NAME ###

Name of the Openstack project. **Required**.

### OS_INTERFACE ###

Openstack interface. Default value is `public`.

### OS_IDENTITY_API_VERSION ###

Version of the Openstack API. Default value is `3`.

### OPENSTACK_FLAVOR ###

Name of the flavor to use for the virtual machines. Default value is `d2-8`.

### OPENSTACK_IMAGE ###

Name of the image to use for the virtual machines. Default value is `Debian 11`.

### OPENSTACK_IP_VERSION ###

IP version to use for virtual machines. Default value is `4`.

### OPENSTACK_NETWORK ###

Name of the network to use for the virtual machines. Default value is `Ext-Net`.

### OPENSTACK_METADATA_KEY ###

Metadata key to identify the scaled server pool. Default value is `group`.

### OPENSTACK_METADATA_VALUE ###

Metadata value to identify the scaled server pool. Default value is `scaler`.

### OPENSTACK_FLOATING_IP_DESCRIPTION ###

Description of the floating IPs that should be assigned (only used when `EXTERNAL_ADDRESS_MANAGEMENT` is enabled). Default value is `server`.

### OPENSTACK_KEYPAIR ###

Name of the keypair that is provisioned on the virtual machines. Optional.

### OPENSTACK_CLOUD_INIT_FILE ###

Path to a cloud-init file to launch on virtual machines at creation. Optional.
