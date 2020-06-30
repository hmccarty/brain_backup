from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="templates")

    with app.app_context():
        from . import routes

        return app