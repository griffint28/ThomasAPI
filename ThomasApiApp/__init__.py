from flask import Flask

from ThomasApiApp import routes, errors


def create_app():
    app = Flask(__name__)

    app.register_blueprint(routes.bp)

    errors.register_error_handlers(app)

    return app
