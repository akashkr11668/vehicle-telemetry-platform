import requests
import random
import time
import os

URL = os.getenv(
    "BACKEND_URL",
    "http://telemetry-backend-service:5000/telemetry"
)

HEADERS = {
    "x-api-key": "supersecretkey",
    "Content-Type": "application/json"
}

while True:

    payload = {
        "vehicle_id": "CAR_001",
        "speed": random.randint(0, 120),
        "engine_temp": random.randint(70, 110),
        "fuel_level": random.randint(-20, 100)
    }

    try:

        response = requests.post(
            URL,
            json=payload,
            headers=HEADERS
        )

        print(
            payload,
            response.status_code
        )

    except Exception as e:

        print(e)

    time.sleep(1)