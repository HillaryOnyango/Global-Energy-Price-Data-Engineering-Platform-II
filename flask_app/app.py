from flask import Flask, render_template

from flask_app.routes.api import api_bp
from app.services.reporting import ReportingService


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(api_bp)

    @app.get("/")
    def dashboard():
        service = ReportingService()
        return render_template(
            "dashboard.html",
            prices=service.latest_prices(limit=25),
            report=service.twenty_four_hour_summary(),
        )

    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
