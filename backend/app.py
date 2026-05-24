from flask import Flask, request, jsonify
import logging
import os
import psycopg2
import time
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# Create logs folder if not exists
os.makedirs("logs", exist_ok=True)

# Logging configuration
logging.basicConfig(
    filename='logs/server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

app = Flask(__name__)

# metrices

telemetry_requests_total = Counter(
    'telemetry_requests_total',
    'Total telemetry requests received'
)

telemetry_failures_total = Counter(
    'telemetry_failures_total',
    'Total failed telemetry requests'
)

# DATABASE CONNECTION RETRY

connection = None

while connection is None:

    try:
        connection = psycopg2.connect(
            host="database",
            database="telemetry",
            user="admin",
            password="password"
        )

        logging.info("Database connected successfully")

    except Exception as error:

        logging.error(f"Database connection failed: {error}")

        print("Database not ready yet... Retrying in 5 seconds")

        time.sleep(5)

cursor = connection.cursor()

# CREATE TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS telemetry_data (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50),
    speed INTEGER,
    fuel_level INTEGER
)
""")

connection.commit()

logging.info("Telemetry table verified successfully")

# VERSION ENDPOINT

@app.route("/version")
def version():

    logging.info("Version endpoint accessed")

    return {
        "version": "1.0.0"
    }

# HOME ENDPOINT

@app.route("/")
def home():

    logging.info("Home endpoint accessed successfully")

    return {
        "message": "Vehicle Telemetry Platform Running"
    }

# TELEMETRY ENDPOINT

@app.route('/telemetry', methods=['POST'])
def telemetry():

    try:

        data = request.get_json()

        required_fields = [
            "vehicle_id",
            "speed",
            "engine_temp",
            "fuel_level"
        ]

        # FIELD VALIDATION

        for field in required_fields:

            if field not in data:

                logging.error(f"Missing field: {field}")

                return jsonify({
                    "error": f"Missing field: {field}"
                }), 400

        # SPEED VALIDATION

        if data["speed"] < 0:

            logging.warning("Invalid speed value detected")

            telemetry_failures_total.inc()

            return jsonify({
                "error": "Invalid speed"
            }), 400

        # FUEL VALIDATION

        if not (0 <= data["fuel_level"] <= 100):

            logging.warning("Invalid fuel level detected")

            telemetry_failures_total.inc()

            return jsonify({
                "error": "Invalid fuel level"
            }), 400

        logging.info(f"Telemetry received: {data}")

        # INSERT INTO DATABASE

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

        logging.info("Telemetry stored successfully")

        telemetry_requests_total.inc()

        return jsonify({
            "message": "Telemetry received successfully"
        }), 200

    except Exception as error:

        logging.error(f"Telemetry processing failed: {error}")

        return jsonify({
            "error": "Internal server error"
        }), 500

# Telemetry History ENDPOINT

@app.route('/telemetry/history')
def telemetry_history():

    try:

        cursor.execute("""
        SELECT vehicle_id, speed, fuel_level
        FROM telemetry_data
        ORDER BY id DESC
        LIMIT 10
        """)

        rows = cursor.fetchall()

        telemetry_history = []

        for row in rows:

            telemetry_history.append({
                "vehicle_id": row[0],
                "speed": row[1],
                "fuel_level": row[2]
            })

        logging.info("Telemetry history fetched successfully")

        return jsonify(telemetry_history), 200

    except Exception as error:

        logging.error(f"Failed to fetch telemetry history: {error}")

        return jsonify({
            "error": "Failed to fetch telemetry history"
        }), 500

# HEALTH ENDPOINT

@app.route("/health")
def health():

    try:

        logging.info("Health check successful")

        return {
            "status": "healthy"
        }

    except Exception as error:

        logging.error(f"Health check failed: {error}")

        return {
            "status": "unhealthy"
        }, 500

# METRICS ENDPOINT

@app.route('/metrics')
def metrics():

    return generate_latest(), 200, {
        'Content-Type': CONTENT_TYPE_LATEST
    }

# APPLICATION START

if __name__ == "__main__":

    logging.info("Starting Vehicle Telemetry Platform")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
