from flask import Blueprint

general_routes = Blueprint(
    'general_routes',
    __name__
)

@general_routes.route("/")
def home():

    return {
        "message": "Vehicle Telemetry Platform Running"
    }

@general_routes.route("/version")
def version():

    return {
        "version": "1.0.0"
    }