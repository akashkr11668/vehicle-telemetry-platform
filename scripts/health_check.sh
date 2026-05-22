#!/bin/bash

FAIL_COUNT=0

while true
do
    STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health)

    TIMESTAMP=$(date)

    if [ "$STATUS_CODE" -eq 200 ]
    then
        echo "$TIMESTAMP Backend is healthy" | tee -a monitoring_logs/health.log

        FAIL_COUNT=0
    else
        echo "$TIMESTAMP Backend is DOWN" | tee -a monitoring_logs/health.log

        FAIL_COUNT=$((FAIL_COUNT + 1))

        echo "Failure Count: $FAIL_COUNT"

        if [ "$FAIL_COUNT" -ge 3 ]
        then
            echo "ALERT: Backend failing repeatedly!"
        fi
    fi

    sleep 5
done