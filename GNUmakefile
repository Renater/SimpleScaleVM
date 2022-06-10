.env:
	cp .env.template .env

env:
	virtualenv env

.PHONY: install
install: env
	env/bin/pip3 install -r requirements.txt

.PHONY: start
start:
	env/bin/python3 src/main.py
