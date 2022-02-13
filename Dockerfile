FROM python:3

RUN apt-get update && apt-get install -y \
    cron
  && rm -rf /var/lib/apt/lists/*

COPY run.sh /run.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /run.sh /entrypoint.sh

COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT /entrypoint.sh
