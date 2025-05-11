FROM python:3.11-slim

RUN pip install --no-cache-dir mpremote

COPY entrypoint.py /entrypoint.py

WORKDIR /src

ENTRYPOINT ["python", "/entrypoint.py"]
