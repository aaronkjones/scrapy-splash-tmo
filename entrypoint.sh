#!/usr/bin/env bash

echo "Container started"

# Setup a cron schedule
echo "*/15 * * * * /run.sh >> /var/log/cron.log 2>&1
#" > scheduler.txt

crontab scheduler.txt
cron -f
