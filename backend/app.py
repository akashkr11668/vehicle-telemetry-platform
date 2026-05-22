from flask import Flask, request, jsonify
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

app = Flask(__name__)

@app.route("/version")
def version():
    logging.info("Version endpoint accessed")
    
    return {
        "version": "1.0.0"
    }


@app.route("/")
def home():
    logging.info("Home endpoint accessed")

    return {
        "message": "Vehicle Telemetry Platform Running"
    }

@app.route('/telemetry', methods=['POST'])
def telemetry():

    data = request.get_json()

    required_fields = [
        "vehicle_id",
        "speed",
        "engine_temp",
        "fuel_level"
    ]

    for field in required_fields:

        if field not in data:

            logging.error(f"Missing field: {field}")

            return jsonify({
                "error": f"Missing field: {field}"
            }), 400
        
    if data["speed"] < 0:
        logging.warning("Invalid speed value")
        return jsonify({
            "error" : "Invalid speed"
        }),400
    
    if not (0 <= data["fuel_level"] <= 100):
        logging.warning("Invalid fuel level")
        return jsonify({
            "error": "Invalid fuel level"
        }), 400


    logging.info(f"Telemetry received: {data}")

    return jsonify({
        "message": "Telemetry received successfully"
    }), 200

@app.route("/health")
def health():
    logging.info("Health endpoint accessed")

    return {
        "status": "healthy"
    }

@app.route('/metrics')
def metrics():
    logging.info("Metrics endpoint accessed")

    return {
        "cpu": "30%",
        "memory": "45%"
    }


if __name__ == "__main__":
    logging.info("Starting Vehicle Telemetry Platform")

    # host="0.0.0.0"	accessible externally
    # port=5000	        explicit port
    # debug=True	    development mode
    app.run(host="0.0.0.0", port=5000, debug=True)