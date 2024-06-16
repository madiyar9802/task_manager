import logging
from flask import jsonify

logger = logging.getLogger('app')


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        logger.error(f"400 Bad Request: {error}")
        return jsonify({'error': 'Bad Request'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        logger.error(f"401 Unauthorized: {error}")
        return jsonify({'error': 'Unauthorized'}), 401

    @app.errorhandler(403)
    def forbidden(error):
        logger.error(f"403 Forbidden: {error}")
        return jsonify({'error': 'Forbidden'}), 403

    @app.errorhandler(404)
    def not_found(error):
        logger.error(f"404 Not Found: {error}")
        return jsonify({'error': 'Not Found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"500 Internal Server Error: {error}")
        return jsonify({'error': 'Internal Server Error'}), 500
