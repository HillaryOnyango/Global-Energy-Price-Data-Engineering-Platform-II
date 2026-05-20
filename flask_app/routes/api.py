from flask import Blueprint, jsonify, request

from app.services.reporting import ReportingService

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.get("/prices")
def prices():
    limit = int(request.args.get("limit", 100))
    return jsonify(ReportingService().latest_prices(limit=limit))

@api_bp.get("/report")
def report():
    return jsonify(ReportingService().twenty_four_hour_summary())
