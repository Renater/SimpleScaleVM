FROM python:3.9.13

LABEL maintainer="contact@renater.fr"

ARG provider=openstack

WORKDIR /requirements

COPY requirements.txt common.txt
COPY src/providers/${provider}/requirements.txt provider.txt
RUN pip install -r common.txt
RUN pip install -r provider.txt

WORKDIR /

COPY src/ /src

EXPOSE 8000

ENTRYPOINT [ "python", "src/main.py" ]
