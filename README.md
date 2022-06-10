# SimpleScaleVM

Python module to manage the autoscaling of a cluster of virtual machines.


## Installation

Python [virtualenv](https://virtualenv.pypa.io/en/latest/) is used to run the module. To install it, launch the following command:

```bash
python3 -m pip install virtualenv
```

To setup the virtualenv and install the requirements, launch the following command:

```bash
make install
```


## Configuration

All the configuration is contained in the `.env` environment file. To initialize it, launch the following command:

```bash
make .env
```

Besides, the following values may be overwritten to configure the module:
* `APP_HOST`: host of the HTTP server.
* `APP_PORT`: port of the HTTP server.


## Launch the module

To start the module, launch the following command:

```bash
make start
```


## Licensing

Apache License Version 2.0.

See [LICENSE](./LICENSE) to see the full text.
