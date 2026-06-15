from flask import Blueprint, jsonify

health_routes = Blueprint(
    'health_routes',
    __name__
)

@health_routes.route("/health")
def health():

    return jsonify({
        "status": "healthy",
        "version": "v2",
        "type": "backend health"
})