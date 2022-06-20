ifneq (,$(wildcard .env))
    include .env
    export
endif


.env:
	cp .env.template .env

env:
	virtualenv env

.PHONY: install
install: env
	env/bin/python3 -m pip install -r requirements.txt
	if [ -f src/providers/${PROVIDER}/requirements.txt ]; then env/bin/python3 -m pip install -r src/providers/${PROVIDER}/requirements.txt; fi

.PHONY: lint
lint:
	env/bin/pylint --ignore-patterns=env/* .

.PHONY: start
start:
	env/bin/python3 src/main.py
