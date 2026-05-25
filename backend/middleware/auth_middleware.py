from flask import request, jsonify
import os

API_KEY = os.getenv("API_KEY")

def require_api_key():

    api_key = request.headers.get("x-api-key")

    if api_key != API_KEY:

        return jsonify({
            "error": "Unauthorized"
        }), 401

    return None