import requests
import random
import time
import logging
import os

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend:5000/telemetry"
)

vehicle_ids = [
    "CAR_001",
    "CAR_002",
    "CAR_003"
]

while True:

    telemetry_data = {
        "vehicle_id": random.choice(vehicle_ids),  # randomly choose vehicle_ids
        "speed": random.randint(0, 150),  # randomly choose values between 0 to 150
        "engine_temp": random.randint(70, 120),
        "fuel_level": random.randint(-20, 120)  #randomly choose values between -20 to 120 but negative gives an err
    }

    # This sends HTTP POST request to backend.
    response = requests.post(
        BACKEND_URL,
        json=telemetry_data
    )

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    logging.info(f"Telemetry Sent: {telemetry_data}")
    logging.info(f"Server Response: {response.json()}")

    #Waits 5 seconds before next telemetry transmission. Without this: simulator would spam thousands of requests instantly.
    time.sleep(5)