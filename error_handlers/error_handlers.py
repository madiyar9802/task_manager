import logging
from flask import jsonify
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError

logger = logging.getLogger('app')


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        logger.error(f'error: {error}')
        response = error.get_response()
        response.data = jsonify({
            "code": error.code,
            "name": error.name,
            "description": error.description
        }).data
        response.content_type = "application/json"
        return response

    @app.errorhandler(Exception)
    def internal_server_error(error):
        logger.error(f"500 Internal Server Error: {error}")
        return jsonify({'error': 'Internal Server Error'}), 500

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        logger.error(f"Database error: {error}")
        response = {
            'error': 'A database error occurred',
            'details': str(error.__cause__) if error.__cause__ else str(error)
        }
        if isinstance(error, IntegrityError):
            response['error'] = 'Integrity error'
        elif isinstance(error, DataError):
            response['error'] = 'Data error'
        return jsonify(response), 400
