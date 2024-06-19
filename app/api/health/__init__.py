from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from app.api.messages import health


blueprint = Blueprint('health_check', __name__, url_prefix='/health_check')
api = Api(blueprint)


@api.resource('')
class HealthResource(Resource):

    def get(self):
        """ Retrieve the health of the endpoint """

        return jsonify({
            'health': health
        })