from flask import Flask

from routes.general_routes import general_routes
from routes.health_routes import health_routes
from routes.telemetry_routes import telemetry_routes
from routes.metrics_routes import metrics_routes

app = Flask(__name__)

# Register Blueprints

app.register_blueprint(general_routes)
app.register_blueprint(health_routes)
app.register_blueprint(telemetry_routes)
app.register_blueprint(metrics_routes)

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )