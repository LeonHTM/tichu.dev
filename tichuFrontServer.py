from flask import Flask,render_template

def create_app():
    app = Flask(__name__, template_folder="routes")

    @app.route("/", methods=["GET"])
    def browser_dashboard():
            return render_template("main.html")
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app

drakynemServer = create_app()

if __name__ == "__main__":
    drakynemServer.run(host="127.0.0.1", port=5012, debug=True)