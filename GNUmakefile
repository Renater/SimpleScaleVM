ifneq (,$(wildcard .env))
    include .env
    export
endif


.env:
	cp .env.template .env

.PHONY: build
build:
	docker build -t renater/simplescalevm:test-${PROVIDER} --build-arg provider=${PROVIDER} .

env:
	virtualenv env

.PHONY: install
install: env
	env/bin/python3 -m pip install -r requirements.txt
	if [ -f src/providers/${PROVIDER}/requirements.txt ]; then env/bin/python3 -m pip install -r src/providers/${PROVIDER}/requirements.txt; fi

.PHONY: lint
lint:
	env/bin/pylint --ignore-patterns=env/* .

.PHONY: release
release: build
	docker tag renater/simplescalevm:test-${PROVIDER} renater/simplescalevm:latest-${PROVIDER}
	docker tag renater/simplescalevm:test-${PROVIDER} renater/simplescalevm:${VERSION}-${PROVIDER}
	docker tag renater/simplescalevm:test-${PROVIDER} renater/simplescalevm:${shell echo ${VERSION} | cut -d '.' -f -2}-${PROVIDER}
	docker tag renater/simplescalevm:test-${PROVIDER} renater/simplescalevm:${shell echo ${VERSION} | cut -d '.' -f -1}-${PROVIDER}
	docker push renater/simplescalevm:latest-${PROVIDER}
	docker push renater/simplescalevm:${VERSION}-${PROVIDER}
	docker push renater/simplescalevm:${shell echo ${VERSION} | cut -d '.' -f -2}-${PROVIDER}
	docker push renater/simplescalevm:${shell echo ${VERSION} | cut -d '.' -f -1}-${PROVIDER}

.PHONY: start
start:
	env/bin/python3 src/main.py

.PHONY: start-docker
start-docker: build
	docker-compose up -d
