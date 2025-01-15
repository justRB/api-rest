from flask_restx import Namespace, Resource, fields
from services.services import generate_stronger_password
from flask import request
from decorators.authentication import auth_required
from config.config import authorizations

api = Namespace('Secure password generation', 'Generate a secure password', authorizations=authorizations)

input_model = api.model(
    "securePasswordGeneration_input", {
        "length": fields.Integer(min=12, max=32, required=True, description="Length of password to generate")
    }
)

message_model = api.model(
    "securePasswordGeneration_output", {
        "message": fields.String(description="Message")
    }
)

class SecurePasswordGenerationAPI(Resource):
    @auth_required
    @api.doc(security='apikey', body=input_model)
    @api.expect(input_model, validate=True)
    @api.response(201, 'Password has been generated', message_model)
    @api.response(400, 'Validation error')
    def post(current_user, *args, **kwargs):
        result = generate_stronger_password(request.get_json(), current_user)
        return result["output"], result["status"]

api.add_resource(SecurePasswordGenerationAPI, "")