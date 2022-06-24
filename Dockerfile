FROM alpine:3.13

RUN apk add --no-cache python3 py3-pip build-base libffi-dev openssl-dev python3-dev musl-dev cargo
RUN pip install --no-cache-dir netmiko 
RUN pip install --no-cache-dir pyyaml mysql-connector-python

ADD . /app

WORKDIR /app

ENTRYPOINT ["python3", "-u", "main.py"]