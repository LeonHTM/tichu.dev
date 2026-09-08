
import requests
from flask import Flask, render_template, send_from_directory
from routes.passkey_routes import passkey_bp


def create_app():

    app = Flask(
        __name__,
        template_folder="routes"
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

        return render_template("main.html")


    @app.route("/privacy", methods=["GET"])
    def privacy():

        return render_template("privacy.html")



    @app.errorhandler(404)
    def page_not_found(e):

        return render_template("404.html"), 404

    return app


tichuFrontServer = create_app()

if __name__ == "__main__":tichuFrontServer.run(
        host="0.0.0.0",
        port=5003,
        debug=True
    )

