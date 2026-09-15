FROM python:3.12-slim

WORKDIR /usr/src/myproject

RUN apt-get update && apt-get install -y --no-install-recommends procps gcc && rm -rf /var/lib/apt/lists/*

COPY lcs /usr/src/lcs
COPY myproject/*.py /usr/src/myproject/
COPY myproject/requirements.txt /usr/src/myproject/
COPY myproject/static /usr/src/myproject/static
COPY myproject/templates /usr/src/myproject/templates

RUN pip install --no-cache-dir /usr/src/lcs \
    && pip install --no-cache-dir -r /usr/src/myproject/requirements.txt

ENTRYPOINT ["python3", "main.py"]
