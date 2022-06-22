ifneq (,$(wildcard .env))
    include .env
    export
endif


.env:
	cp .env.template .env

.PHONY: build
build:
	docker build -t renater/simplescalevm:${PROVIDER}-test --build-arg provider=${PROVIDER} .

env:
	virtualenv env

.PHONY: install
install: env
	env/bin/python3 -m pip install -r requirements.txt
	if [ -f src/providers/${PROVIDER}/requirements.txt ]; then env/bin/python3 -m pip install -r src/providers/${PROVIDER}/requirements.txt; fi

.PHONY: lint
lint:
	env/bin/pylint --ignore-patterns=env/* .

.PHONY: mock
mock: tests/mock.env
	python3 tests/mock.py

.PHONY: release
release: build
	docker tag renater/simplescalevm:${PROVIDER}-test renater/simplescalevm:${PROVIDER}-latest
	docker tag renater/simplescalevm:${PROVIDER}-test renater/simplescalevm:${PROVIDER}-${VERSION}
	docker tag renater/simplescalevm:${PROVIDER}-test renater/simplescalevm:${PROVIDER}-${shell echo ${VERSION} | cut -d '.' -f -2}
	docker tag renater/simplescalevm:${PROVIDER}-test renater/simplescalevm:${PROVIDER}-${shell echo ${VERSION} | cut -d '.' -f -1}
	docker push renater/simplescalevm:${PROVIDER}-latest
	docker push renater/simplescalevm:${PROVIDER}-${VERSION}
	docker push renater/simplescalevm:${PROVIDER}-${shell echo ${VERSION} | cut -d '.' -f -2}
	docker push renater/simplescalevm:${PROVIDER}-${shell echo ${VERSION} | cut -d '.' -f -1}

.PHONY: start
start:
	env/bin/python3 src/main.py

.PHONY: start-docker
start-docker: build
	docker-compose up -d

tests/mock.env:
	cp tests/mock.env.template tests/mock.env
