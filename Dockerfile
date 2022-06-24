FROM python:3.9.13

LABEL maintainer="contact@renater.fr"

ARG provider=openstack

RUN useradd -m -s /bin/sh -d /src scaler
USER scaler

WORKDIR /requirements

COPY --chown=scaler requirements.txt common.txt
COPY --chown=scaler src/providers/${provider}/requirements.txt provider.txt
RUN pip install -r common.txt
RUN pip install -r provider.txt

WORKDIR /

COPY --chown=scaler src/ /src

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

ENTRYPOINT [ "python", "src/main.py" ]
