import logging
from flask import has_request_context, request, g
from flask.logging import default_handler


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.username = 'Unknown' if g.username is None else g.username

        return super().format(record)


formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s %(username)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(formatter)
