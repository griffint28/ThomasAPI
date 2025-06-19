from flask import jsonify


def register_error_handlers(app):  # Takes the app instance
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(error=str(error)), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(error=str(error)), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify(error=str(error)), 401


