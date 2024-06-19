from __future__ import absolute_import

from datetime import datetime
import logging
import json

from flask import current_app
from flask import request
from flask import g
from flask import has_request_context

from app.api.utils import request_ids


def setup_logging(app):
    class ApiFilter(logging.Filter):
        def filter(self, record):
            record.environment = app.config.get('ENVIRONMENT')
            if has_request_context():
                request_id, original_request_id = request_ids()
                record.request_id = request_id
                record.original_request_id = original_request_id
                record.request_url = request.url
                record.request_method = request.method
                record.remote_addr = request.remote_addr
                record.endpoint = request.endpoint
            return True

    app.logger.addFilter(ApiFilter())

    @app.before_request
    def log_request_info():
        g.start = datetime.now()

        request_id, original_request_id = request_ids()
        log_data = {'request-id': str(request_id),
                    'original-request-id': original_request_id,
                    'user-agent': request.headers.get('User-Agent'),
                    'url': request.url}
        
        try:
            json_data = request.json
        except Exception:
            json_data = {}

        log_data['json_data'] = json_data
        current_app.logger.info('Request Data: {0}'.format(log_data))

    @app.after_request
    def log_response_info(response):
        time = datetime.now() - g.start
        request_id, original_request_id = request_ids()

        log_data = {'url': request.url,
                    'response_code': response.status_code,
                    'time': time.seconds + time.microseconds / 10. ** 6,
                    'request-id': str(request_id),
                    'original-request-id': original_request_id}

        try:
            data = json.loads(response.data)
        except ValueError:
            data = {}

        log_data['data'] = data

        current_app.logger.info('Response Data: {0}'.format(log_data))
        return response
