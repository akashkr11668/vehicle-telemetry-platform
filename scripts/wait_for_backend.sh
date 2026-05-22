#!/bin/bash

MAX_RETRIES=5

RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]
do
    STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health)

    if [ "$STATUS_CODE" -eq 200 ]
    then
        echo "Backend is healthy"

        exit 0
    fi

    RETRY_COUNT=$((RETRY_COUNT + 1))

    echo "Backend not ready yet..."
    echo "Retry: $RETRY_COUNT"

    sleep 5
done

echo "Backend failed after maximum retries"

exit 1