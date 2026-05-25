from flask import (
    Blueprint,
    request,
    jsonify
)

from middleware.auth_middleware import require_api_key

import logging

from services.telemetry_service import process_telemetry

from database.db import cursor

telemetry_routes = Blueprint(
    'telemetry_routes',
    __name__
)

# -----------------------------------
# TELEMETRY INGESTION
# -----------------------------------

@telemetry_routes.route('/telemetry', methods=['POST'])
def telemetry():

    auth_error = require_api_key()

    if auth_error:
        return auth_error

    try:

        data = request.get_json()

        response, status_code = process_telemetry(data)

        return jsonify(response), status_code

    except Exception as error:

        logging.error(f"Telemetry processing failed: {error}")

        return jsonify({
            "error": "Internal server error"
        }), 500

# -----------------------------------
# TELEMETRY HISTORY
# -----------------------------------

@telemetry_routes.route('/telemetry/history')
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