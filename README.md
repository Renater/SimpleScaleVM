# SimpleScaleVM

This repository hosts a Python module to manage the autoscaling of a cluster of virtual instances called **replicas**. The full explanation of the functioning of this module is described in [the documentation directory](./docs/simplescalevm-in-depth.md).


## Configuration

All the configuration is contained in the `.env` environment file. To initialize it, launch the following command:

```bash
make .env
```

The precise description of all environment variables that are used to configure the Scaler is available in [the Docker image README](./docs/dockerhub.readme.md) and on [DockerHub](https://hub.docker.com/repository/docker/renater/simplescalevm/general), in the corresponding subsection.

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

Note that each provider has its specific Docker image version which contains the provider requirements: the Docker tag format is `<provider>-<version>`. In order to release a specific version of the module, you may modify the `VERSION` and `PROVIDER` environment variables.

The full documentation of the SimpleScaleVM Docker image is available on [DockerHub](https://hub.docker.com/repository/docker/renater/simplescalevm/general).


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
