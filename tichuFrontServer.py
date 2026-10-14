import requests
from flask import (
    Flask,
    render_template,
    send_from_directory,
    request,
    redirect,
    url_for,
)
from routes.passkey_routes import passkey_bp
from config import SUPPORTED_LANGUAGES


def detect_language():
    first_segment = request.path.strip("/").split("/")[0]
    if first_segment in SUPPORTED_LANGUAGES:
        return first_segment
    # 1. /langugage
    # 2. Browser preference
    # 3. Default
    return request.accept_languages.best_match(SUPPORTED_LANGUAGES) or "en"


def create_app():
    app = Flask(
        __name__,
        template_folder="templates"
    )

    app.register_blueprint(passkey_bp)

    @app.route("/.well-known/apple-app-site-association")
    def apple_app_site_association():
        return send_from_directory(
            "/Users/leon/Desktop/TichuServer/.well-known",
            "apple-app-site-association",
            mimetype="application/json"
        )

    @app.route("/", methods=["GET"])
    def browser_dashboard():
        lang = request.accept_languages.best_match(
            SUPPORTED_LANGUAGES
        ) or "en"

        return redirect(url_for("localized_dashboard", lang=lang))


    @app.route("/<lang>", methods=["GET"])
    def localized_dashboard(lang):
        if lang not in SUPPORTED_LANGUAGES:
            return render_template("404.html", lang=detect_language()), 404

        return render_template("main.html", lang=lang)

    @app.route("/privacy", methods=["GET"])
    def privacy():
        lang = request.accept_languages.best_match(
                    SUPPORTED_LANGUAGES
                ) or "en"

        return redirect(url_for("localized_privacy", lang=lang))

    @app.route("/<lang>/privacy", methods=["GET"])
    def localized_privacy(lang):
        if lang not in SUPPORTED_LANGUAGES:
            return render_template("404.html", lang=detect_language()), 404

        return render_template("privacy.html", lang=lang)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html", lang=detect_language()), 404
                

    LANGUAGE_NAMES = {"en": "🇬🇧 English", "de": "🇩🇪 Deutsch", "el": "🇬🇷 Ελληνικά"}

    @app.context_processor
    def inject_language_links():
        parts = request.path.strip("/").split("/", 1)
        # keep the sub-page (e.g. "privacy") only on real, matched routes
        rest = parts[1] if len(parts) > 1 and parts[0] in SUPPORTED_LANGUAGES and request.endpoint else ""
        return {
            "language_links": [
                {
                    "code": code,
                    "name": LANGUAGE_NAMES.get(code, code.upper()),
                    "url": f"/{code}/{rest}".rstrip("/"),
                }
                for code in SUPPORTED_LANGUAGES
            ]
        }

    

    return app


tichuFrontServer = create_app()

if __name__ == "__main__":
    tichuFrontServer.run(
        host="0.0.0.0",
        port=5003,
        debug=True
    )