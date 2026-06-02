import logging

from database.db import connection, cursor

from monitoring.metrics import (
    telemetry_requests_total,
    telemetry_failures_total
)



def process_telemetry(data):

    logging.error(f"PAYLOAD RECEIVED: {data}")

    required_fields = [
        "vehicle_id",
        "speed",
        "engine_temp",
        "fuel_level"
    ]

    # -----------------------------
    # FIELD VALIDATION
    # -----------------------------

    for field in required_fields:

        if field not in data:

            telemetry_failures_total.inc()

            logging.error(f"Missing field: {field}")

            return {
                "error": f"Missing field: {field}"
            }, 400

    # -----------------------------
    # SPEED VALIDATION
    # -----------------------------

    if data["speed"] < 0:

        telemetry_failures_total.inc()

        logging.warning("Invalid speed value detected")

        return {
            "error": "Invalid speed"
        }, 400

    # -----------------------------
    # FUEL VALIDATION
    # -----------------------------

    if not (0 <= data["fuel_level"] <= 100):

        telemetry_failures_total.inc()

        logging.warning("Invalid fuel level detected")

        return {
            "error": "Invalid fuel level"
        }, 400

    # -----------------------------
    # INSERT INTO DATABASE
    # -----------------------------

    cursor.execute(
        """
        INSERT INTO telemetry_data (
            vehicle_id,
            speed,
            fuel_level
        )
        VALUES (%s, %s, %s)
        """,
        (
            data["vehicle_id"],
            data["speed"],
            data["fuel_level"]
        )
    )

    connection.commit()

    telemetry_requests_total.inc()

    logging.info("Telemetry stored successfully")

    return {
        "message": "Telemetry received successfully"
    }, 200