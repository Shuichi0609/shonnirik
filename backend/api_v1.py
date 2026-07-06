from flask import Blueprint, request, jsonify
from PIL import Image
import logging

from utils.patient_db import (
    get_dashboard_stats,
    list_studies,
)

from core.inference import predict_image

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
logger = logging.getLogger("api_v1")


@api_v1.route("/predict", methods=["POST"])
def api_predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        img = Image.open(file.stream).convert("RGB")

        result, _ = predict_image(img)

        return jsonify(result)

    except Exception as e:
        logger.exception("Prediction failed")
        return jsonify({"error": str(e)}), 500


@api_v1.route("/studies", methods=["GET"])
def api_studies():
    try:
        studies = list_studies()
        return jsonify({"data": studies})
    except Exception as e:
        logger.error(f"API /studies error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@api_v1.route("/analytics", methods=["GET"])
def api_analytics():
    try:
        stats = get_dashboard_stats()
        return jsonify({"data": stats})
    except Exception as e:
        logger.error(f"API /analytics error: {e}")
        return jsonify({"error": "Internal server error"}), 500