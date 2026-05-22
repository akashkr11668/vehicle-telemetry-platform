    #!/bin/bash

    PROJECT_NAME="Vehicle Telemetry Platform"

    echo "Starting $PROJECT_NAME..."

    if docker info > /dev/null 2>&1
    then
        echo "Docker is running"
    else
        echo "Docker is NOT running"
    exit 1
fi

    docker compose up --build