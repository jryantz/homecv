from flask import Blueprint, jsonify
import time

blueprint = Blueprint("health", __name__)


@blueprint.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for container monitoring"""
    try:
        return (
            jsonify(
                {
                    "status": "healthy",
                    "timestamp": time.time(),
                    "service": "homecv",
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": time.time(),
                    "service": "homecv",
                }
            ),
            503,
        )
