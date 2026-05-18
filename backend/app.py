from flask import Flask
import logging

logging.basicConfig(
    filename='logs/server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

app = Flask(__name__)

@app.route("/")
def home():
    logging.info("Home endpoint accessed")

    return {
        "message": "Vehicle Telemetry Platform Running"
    }

@app.route("/health")
def health():
    logging.info("Health endpoint accessed")

    return {
        "status": "healthy"
    }

if __name__ == "__main__":
    logging.info("Starting Vehicle Telemetry Platform")

    app.run(debug=True)